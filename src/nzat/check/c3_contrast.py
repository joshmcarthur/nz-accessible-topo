from nzat.style.text_audit import text_audit

TEXT_ALLOWLIST = {"All-Highway-Labels-three", "All-Highway-Labels-standard"}


def c3_contrast(style, variant):
    failures = []
    for lid, cr, *_ in text_audit(style, (255, 255, 255)):
        if cr < 4.5 and lid not in TEXT_ALLOWLIST:
            failures.append(f"C3: {variant}:{lid} text contrast {cr:.2f}")
    return failures
