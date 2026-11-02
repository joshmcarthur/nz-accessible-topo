#!/usr/bin/env python3
"""Fit flat carto_text names where their labels collide, and write carto_fit.json.

QGIS tests label boxes as yes or no, so it cannot choose the position with the least ink overlap.
This tool renders the map face, finds flat names whose boxes collide, and tries each one on one
line or in its default form, moved in small steps. It scores glyph ink and halo, not boxes.
Flat names are drawn as glyphs. Every other label is its QGIS box. Point symbols are not counted.

Run it with the QGIS Python on the accessible project, then run the apply step again:

    python fit_carto_labels.py --project accessible/nztopo50.qgs --font fonts \
        --extent 1564000,5154000,1588000,5190000
"""

import argparse
import json
import math
import os
import sys

import numpy as np

import override_topo50_project as ov
import render_square as rs

METRES_PER_PX = 2.0
PX_PER_MM = ov.SHEET_SCALE / 1000 / METRES_PER_PX
STEP_MM = 0.25
REACH_X_MM = 1.5
REACH_Y_MM = 0.5
INK_WEIGHT = 10
HALO_WEIGHT = 3
MOVE_COST_PER_MM = 40
PASSES = 3
FACE_DPI = 150


def overlap_score(target_ink, target_halo, near_ink, near_halo, col, row):
    """Ink on ink counts INK_WEIGHT times, ink inside a halo HALO_WEIGHT times, and halo on halo once."""
    height, width = target_ink.shape
    if col < 0 or row < 0 or row + height > near_ink.shape[0] or col + width > near_ink.shape[1]:
        return math.inf
    ink = near_ink[row : row + height, col : col + width]
    halo = near_halo[row : row + height, col : col + width]
    return (
        INK_WEIGHT * int(np.count_nonzero(target_ink & ink))
        + HALO_WEIGHT * int(np.count_nonzero(target_halo & ink))
        + HALO_WEIGHT * int(np.count_nonzero(target_ink & halo))
        + int(np.count_nonzero(target_halo & halo))
    )


def best_candidate(candidates, near_ink, near_halo):
    """Return the candidate with the lowest overlap plus move cost.

    Each candidate is (key, ink, halo, col, row, move_mm).
    """
    return min(
        candidates,
        key=lambda c: overlap_score(c[1], c[2], near_ink, near_halo, c[3], c[4]) + MOVE_COST_PER_MM * c[5],
    )


def stamp(canvas, mask, col, row):
    height, width = mask.shape
    top, left = max(row, 0), max(col, 0)
    bottom, right = min(row + height, canvas.shape[0]), min(col + width, canvas.shape[1])
    if top < bottom and left < right:
        canvas[top:bottom, left:right] |= mask[top - row : bottom - row, left - col : right - col]


def steps_mm(low, high):
    """Steps of STEP_MM from low to high that include 0, so a name with no overlap stays put."""
    return np.concatenate((-np.arange(0, -low + STEP_MM / 2, STEP_MM)[::-1], np.arange(STEP_MM, high + STEP_MM / 2, STEP_MM)))


def main():
    os.environ.setdefault("HOME", "/tmp")
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    parser = argparse.ArgumentParser(description="Write carto_fit.json for flat carto_text names that collide.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--font", action="append", default=[])
    parser.add_argument("--extent", required=True, help="XMIN,YMIN,XMAX,YMAX in EPSG:2193")
    args = parser.parse_args()
    extent = [float(value) for value in args.extent.split(",")]

    # QGIS is only in the QGIS Python. Tests import this module on the host for the scoring.
    from qgis.core import (  # noqa: E402
        QgsApplication,
        QgsCoordinateReferenceSystem,
        QgsExpression,
        QgsExpressionContext,
        QgsExpressionContextUtils,
        QgsMapRendererSequentialJob,
        QgsMapSettings,
        QgsPalLabeling,
        QgsPalLayerSettings,
        QgsProject,
        QgsRectangle,
        QgsRenderContext,
        QgsTextFormat,
        QgsTextRenderer,
        Qgis,
    )
    from qgis.PyQt.QtCore import QRectF, QSize  # noqa: E402
    from qgis.PyQt.QtGui import QFontDatabase, QImage, QPainter  # noqa: E402

    QgsApplication.setPrefixPath(rs.qgis_prefix(os.environ.get("QGIS_PREFIX_PATH")), True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    try:
        for path in rs.font_files(args.font):
            if QFontDatabase.addApplicationFont(path) < 0:
                print(f"font not loaded: {path}", file=sys.stderr)
                return 1
        project = QgsProject.instance()
        if not project.read(args.project):
            print(f"failed to read {args.project}", file=sys.stderr)
            return 1
        layers = rs.map_layers(project)
        carto = next(layer for layer in layers if layer.name() == ov.CARTO_TEXT_LAYER)
        flat_settings = carto.labeling().rootRule().children()[1].settings()
        context = QgsExpressionContext()
        context.appendScope(QgsExpressionContextUtils.globalScope())
        context.appendScope(QgsExpressionContextUtils.projectScope(project))
        context.appendScope(QgsExpressionContextUtils.layerScope(carto))

        settings = QgsMapSettings()
        settings.setLayers(layers)
        settings.setDestinationCrs(QgsCoordinateReferenceSystem.fromEpsgId(2193))
        settings.setExtent(QgsRectangle(*extent))
        width_mm = (extent[2] - extent[0]) / ov.SHEET_SCALE * 1000
        height_mm = (extent[3] - extent[1]) / ov.SHEET_SCALE * 1000
        settings.setOutputSize(QSize(round(width_mm / 25.4 * FACE_DPI), round(height_mm / 25.4 * FACE_DPI)))
        settings.setOutputDpi(FACE_DPI)
        settings.setExpressionContext(context)
        settings.setLabelingEngineSettings(project.labelingEngineSettings())
        job = QgsMapRendererSequentialJob(settings)
        job.start()
        job.waitForFinished()
        placed = [label for label in job.takeLabelingResults().allLabels() if not label.isUnplaced]

        flat_filter = QgsExpression(ov.CARTO_POINT_FILTER)
        props = flat_settings.dataDefinedProperties()
        P = QgsPalLayerSettings.Property

        def text_format(feature_context):
            fmt = QgsTextFormat(flat_settings.format())
            fmt.setSize(props.valueAsDouble(P.Size, feature_context, fmt.size())[0])
            buffer = fmt.buffer()
            buffer.setSize(props.valueAsDouble(P.BufferSize, feature_context, buffer.size())[0])
            fmt.setBuffer(buffer)
            return fmt

        def masks(fmt, lines):
            """Return (ink, halo, margin) masks of the label box at METRES_PER_PX."""
            image_masks = []
            for halo in (False, True):
                layer_fmt = QgsTextFormat(fmt)
                buffer = layer_fmt.buffer()
                buffer.setEnabled(halo)
                layer_fmt.setBuffer(buffer)
                probe = QImage(1, 1, QImage.Format.Format_ARGB32)
                painter = QPainter(probe)
                rc = QgsRenderContext.fromQPainter(painter)
                rc.setScaleFactor(PX_PER_MM)
                rc.setRendererScale(ov.SHEET_SCALE)
                width = QgsTextRenderer.textWidth(rc, layer_fmt, lines)
                height = QgsTextRenderer.textHeight(rc, layer_fmt, lines, Qgis.TextLayoutMode.Rectangle)
                painter.end()
                margin = math.ceil(buffer.size() * PX_PER_MM) + 2
                image = QImage(math.ceil(width) + 2 * margin, math.ceil(height) + 2 * margin, QImage.Format.Format_ARGB32)
                image.fill(0)
                painter = QPainter(image)
                rc = QgsRenderContext.fromQPainter(painter)
                rc.setScaleFactor(PX_PER_MM)
                rc.setRendererScale(ov.SHEET_SCALE)
                QgsTextRenderer.drawText(
                    QRectF(margin, margin, width, height), 0, Qgis.TextHorizontalAlignment.Center,
                    lines, rc, layer_fmt, True, Qgis.TextVerticalAlignment.Bottom,
                )
                painter.end()
                bits = image.constBits()
                bits.setsize(image.sizeInBytes())
                argb = np.frombuffer(bits, np.uint8).reshape(image.height(), image.bytesPerLine())
                alpha = argb[:, 3 : image.width() * 4 : 4] > 64
                image_masks.append((alpha.copy(), width, height, margin))
            (ink, width, height, margin), (halo, _, _, _) = image_masks
            return ink, halo, width, height, margin

        movers = {}
        for label in placed:
            if label.layerID != carto.id():
                continue
            feature = carto.getFeature(label.featureId)
            feature_context = QgsExpressionContext(context)
            feature_context.setFeature(feature)
            if not flat_filter.evaluate(feature_context):
                continue
            wrap = props.valueAsInt(P.AutoWrapLength, feature_context, 0)[0]
            fmt = text_format(feature_context)
            forms = {2: QgsPalLabeling.splitToLines(label.labelText, "", wrap, True)}
            one_line = feature["text_string"]
            if forms[2] != [one_line]:
                forms[1] = [one_line]
            rect = label.labelRect
            _, _, width, height, _ = masks(fmt, forms[2])
            if abs(width * METRES_PER_PX / rect.width() - 1) > 0.05 or abs(height * METRES_PER_PX / rect.height() - 1) > 0.05:
                print(f"mask {width * METRES_PER_PX:.0f}x{height * METRES_PER_PX:.0f} m differs from box "
                      f"{rect.width():.0f}x{rect.height():.0f} m: {label.labelText!r}")
            movers[label] = {
                "id": feature["id"],
                "stock": (rect.center().x(), rect.yMinimum()),
                "at": (rect.center().x(), rect.yMinimum()),
                "lines": 2,
                "forms": {lines: masks(fmt, text) for lines, text in forms.items()},
            }

        def to_px(window, x, y):
            return round((x - window[0]) / METRES_PER_PX), round((window[3] - y) / METRES_PER_PX)

        def stamp_label(ink_canvas, halo_canvas, window, other):
            if other in movers:
                info = movers[other]
                ink, halo, width, height, margin = info["forms"][info["lines"]]
                col, row = to_px(window, *info["at"])
                col -= round(margin + width / 2)
                row -= round(margin + height)
                stamp(ink_canvas, ink, col, row)
                stamp(halo_canvas, halo, col, row)
                return
            box = other.labelRect
            left, top = to_px(window, box.xMinimum(), box.yMaximum())
            right, bottom = to_px(window, box.xMaximum(), box.yMinimum())
            block = np.ones((max(bottom - top, 1), max(right - left, 1)), bool)
            stamp(ink_canvas, block, left, top)
            stamp(halo_canvas, block, left, top)

        colliding = [
            label for label in movers
            if any(other is not label and other.labelRect.intersects(label.labelRect) for other in placed)
        ]
        print(f"flat names {len(movers)}; colliding {len(colliding)}")
        reach_x = REACH_X_MM * PX_PER_MM * METRES_PER_PX
        for _ in range(PASSES):
            for label in colliding:
                info = movers[label]
                sx, sy = info["stock"]
                tallest = max(form[3] for form in info["forms"].values()) * METRES_PER_PX
                window = (sx - 1500 - reach_x, sy - tallest - 400, sx + 1500 + reach_x, sy + tallest + 400)
                shape = (round((window[3] - window[1]) / METRES_PER_PX), round((window[2] - window[0]) / METRES_PER_PX))
                near_ink, near_halo = np.zeros(shape, bool), np.zeros(shape, bool)
                area = QgsRectangle(*window)
                for other in placed:
                    if other is not label and other.labelRect.intersects(area):
                        stamp_label(near_ink, near_halo, window, other)
                candidates = []
                for lines, (ink, halo, width, height, margin) in info["forms"].items():
                    lowest_mm = -height / PX_PER_MM - REACH_Y_MM
                    for dx_mm in steps_mm(-REACH_X_MM, REACH_X_MM):
                        for dy_mm in steps_mm(lowest_mm, REACH_Y_MM):
                            x = sx + dx_mm * ov.SHEET_SCALE / 1000
                            y = sy + dy_mm * ov.SHEET_SCALE / 1000
                            col, row = to_px(window, x, y)
                            move_mm = math.hypot(dx_mm, dy_mm)
                            candidates.append(((lines, x, y), ink, halo,
                                               col - round(margin + width / 2), row - round(margin + height), move_mm))
                (lines, x, y), *_ = best_candidate(candidates, near_ink, near_halo)
                info["lines"], info["at"] = lines, (x, y)

        fit = {}
        for label in colliding:
            info = movers[label]
            if info["lines"] != 2 or info["at"] != info["stock"]:
                fit[info["id"]] = {"x": round(info["at"][0], 1), "y": round(info["at"][1], 1), "lines": info["lines"]}
                print(f"fit {label.labelText!r}: lines {info['lines']} at {fit[info['id']]['x']}, {fit[info['id']]['y']}")
        output = os.path.join(os.path.dirname(os.path.abspath(args.project)), ov.CARTO_FIT_FILE)
        with open(output, "w", encoding="utf-8") as handle:
            json.dump(fit, handle, indent=2, sort_keys=True)
        print(f"wrote {output} ({len(fit)} names)")
    finally:
        qgs.exitQgis()
    return 0


if __name__ == "__main__":
    sys.exit(main())
