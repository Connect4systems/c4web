from pathlib import Path
import re

ROOT = Path("c4web/www")

HEAD_BLOCK = """    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-PCBW39D2');</script>
    <!-- End Google Tag Manager -->
    <!-- Google tag (gtag.js) - Google Ads -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=AW-1001473338"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'AW-1001473338');
      gtag('config', 'G-LFTCBTF7QL');
    </script>
    <!-- End Google tag -->
"""

BODY_BLOCK = """    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PCBW39D2"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->
"""

def normalize_file(path: Path) -> bool:
    s = path.read_text(encoding="utf-8", errors="ignore")
    original = s

    # Remove first head GTM+gtag block if present
    s = re.sub(
        r"\s*<!-- Google Tag Manager -->[\s\S]*?<!-- End Google tag -->\s*",
        "\n",
        s,
        count=1,
    )

    # Remove first body noscript block if present
    s = re.sub(
        r"\s*<!-- Google Tag Manager \(noscript\) -->[\s\S]*?<!-- End Google Tag Manager \(noscript\) -->\s*",
        "\n",
        s,
        count=1,
    )

    # Inject canonical blocks
    s = re.sub(r"(<head[^>]*>\s*)", r"\1\n" + HEAD_BLOCK, s, count=1, flags=re.IGNORECASE)
    s = re.sub(r"(<body[^>]*>\s*)", r"\1\n" + BODY_BLOCK, s, count=1, flags=re.IGNORECASE)

    if s != original:
        path.write_text(s, encoding="utf-8", newline="\n")
        return True
    return False


def validate_file(path: Path):
    s = path.read_text(encoding="utf-8", errors="ignore")
    l = s.lower()

    h = l.find("<head")
    b = l.find("<body")
    gtm = l.find("googletagmanager.com/gtm.js?id=")
    gtag = l.find("googletagmanager.com/gtag/js?id=aw-1001473338")
    ns = l.find("googletagmanager.com/ns.html?id=gtm-pcbw39d2")
    be = l.find(">", b) if b != -1 else -1

    checks = {
        "head_before_body": (h != -1 and b != -1 and h < b),
        "gtm_in_head": (gtm != -1 and h != -1 and b != -1 and h < gtm < b),
        "gtag_in_head": (gtag != -1 and h != -1 and b != -1 and h < gtag < b),
        "noscript_in_body": (ns != -1 and b != -1 and ns > b),
        "noscript_after_body_open": (ns != -1 and be != -1 and be < ns < be + 1600),
    }
    return checks


def main():
    files = sorted(ROOT.glob("*.html"))
    changed = []

    for f in files:
        if normalize_file(f):
            changed.append(f.name)

    bad = []
    for f in files:
        checks = validate_file(f)
        if not all(checks.values()):
            bad.append((f.name, [k for k, v in checks.items() if not v]))

    print(f"TOTAL {len(files)}")
    print(f"CHANGED {len(changed)}")
    for name in changed:
        print(f"CHANGED_FILE {name}")
    print(f"BAD {len(bad)}")
    for name, issues in bad:
        print(f"BAD_FILE {name} :: {','.join(issues)}")


if __name__ == "__main__":
    main()
