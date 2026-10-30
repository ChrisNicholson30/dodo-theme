"""The Dodo palette — single source of truth for every editor & terminal.

Five variants, three dark and two light. They share one idea: a quiet,
neutral grey canvas with a whisper of temperature (no heavy tint washing
over the screen), and colour that lives in the *code*, borrowed from the
dodo itself:

    feather   slate-blue plumage         → folders, properties, links
    beak      honey-gold upper bill      → functions (in every variant)
    ember     Claude coral / terracotta  → the house accent
    belly     warm cream                 → foreground text
    lagoon    Mauritius sea teal         → types
    eye       cinnamon brown             → parameters

Each variant re-ranks those hues around its own accent so the family is
recognisably related but never just a brightness slider.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Variant:
    slug: str
    name: str
    appearance: str  # "dark" | "light"
    tagline: str
    ui: dict[str, str]
    accent: str
    feather: str
    syntax: dict[str, str]
    ansi: dict[str, str]
    status: dict[str, str]
    icons: dict[str, str]
    players: list[str] = field(default_factory=list)

    @property
    def is_dark(self) -> bool:
        return self.appearance == "dark"


# ---------------------------------------------------------------------------
#  DUSK — the Claude Dark homage. Warm charcoal, coral keywords.
# ---------------------------------------------------------------------------
DUSK = Variant(
    slug="dusk",
    name="Dodo Dusk",
    appearance="dark",
    tagline="Warm charcoal & Claude coral — the original.",
    ui=dict(
        crust="#1a1918",
        mantle="#1f1e1d",
        base="#262624",
        surface0="#2c2b29",
        surface1="#343330",
        surface2="#3e3c38",
        border="#33322f",
        border_variant="#2b2a28",
        text="#ebe7de",
        subtext="#bcb7ab",
        muted="#8c877c",
        faint="#5f5b54",
    ),
    accent="#d97757",
    feather="#8f9fca",
    syntax=dict(
        keyword="#e0896a",
        function="#e8b96e",
        type="#7ec6b7",
        string="#aac68c",
        number="#bea5ea",
        constant="#bea5ea",
        property="#a3b5e8",
        parameter="#e6caa6",
        variable="#ebe7de",
        variable_special="#e7929d",
        operator="#8fc3dc",
        punctuation="#8e897e",
        bracket="#a39e92",
        comment="#827d73",
        comment_doc="#99937f",
        tag="#e0896a",
        attribute="#e8b96e",
        namespace="#a6d4cb",
        string_escape="#e7929d",
        regex="#8fc3dc",
        string_special="#e6caa6",
        heading="#e0896a",
        link="#a3b5e8",
        link_uri="#7ec6b7",
        list_marker="#e0896a",
        selector="#e8b96e",
        selector_pseudo="#bea5ea",
        literal="#aac68c",
        preproc="#e7929d",
        label="#a3b5e8",
    ),
    ansi=dict(
        black="#3b3a36", red="#e57a6c", green="#a9c58b", yellow="#e8b96e",
        blue="#93a8e6", magenta="#c5a3ea", cyan="#7ec6b7", white="#d9d4c9",
        bright_black="#706b62", bright_red="#f0948a", bright_green="#bfd8a3",
        bright_yellow="#f3cd8d", bright_blue="#afc0f2", bright_magenta="#d8bdf3",
        bright_cyan="#9edbcf", bright_white="#f6f3ec",
    ),
    status=dict(
        error="#e57a6c", warning="#e8b96e", info="#93a8e6", success="#a9c58b",
        hint="#8fa6c9", added="#a9c58b", modified="#e8b96e", deleted="#e57a6c",
        renamed="#8fc3dc", conflict="#e7929d",
    ),
    icons=dict(
        blue="#86a6e8", sky="#83c2e0", teal="#71c2b3", green="#a5c886",
        lime="#c3d27c", yellow="#ecc56e", amber="#e9a55c", orange="#e0875f",
        red="#e3726a", pink="#e690a6", purple="#b99be6", lavender="#a9a8ec",
        brown="#c09a78", gray="#8e897f", cream="#e3d8c2",
    ),
)

# ---------------------------------------------------------------------------
#  NIGHT — a cooler, deeper slate. Feather-blue keywords, beak-gold calls.
# ---------------------------------------------------------------------------
NIGHT = Variant(
    slug="night",
    name="Dodo Night",
    appearance="dark",
    tagline="Cool slate plumage after sundown.",
    ui=dict(
        crust="#121316",
        mantle="#16171b",
        base="#1b1c21",
        surface0="#212228",
        surface1="#292b32",
        surface2="#33353e",
        border="#2a2c33",
        border_variant="#212228",
        text="#e0e2ea",
        subtext="#b0b4c3",
        muted="#808599",
        faint="#545969",
    ),
    accent="#8fa6ee",
    feather="#8fa6ee",
    syntax=dict(
        keyword="#94a9f2",
        function="#f0c27b",
        type="#6ccfc2",
        string="#a2d39b",
        number="#f29d86",
        constant="#f29d86",
        property="#c8b5f3",
        parameter="#ead0a9",
        variable="#e0e2ea",
        variable_special="#f08fab",
        operator="#86c8e8",
        punctuation="#7d8295",
        bracket="#9599aa",
        comment="#6c7186",
        comment_doc="#838aa2",
        tag="#94a9f2",
        attribute="#f0c27b",
        namespace="#9fdcd3",
        string_escape="#f08fab",
        regex="#86c8e8",
        string_special="#ead0a9",
        heading="#94a9f2",
        link="#c8b5f3",
        link_uri="#6ccfc2",
        list_marker="#94a9f2",
        selector="#f0c27b",
        selector_pseudo="#c8b5f3",
        literal="#a2d39b",
        preproc="#f08fab",
        label="#c8b5f3",
    ),
    ansi=dict(
        black="#33363f", red="#f07c7c", green="#a2d39b", yellow="#f0c27b",
        blue="#8fa6ee", magenta="#c8a6f2", cyan="#6ccfc2", white="#d4d7e1",
        bright_black="#666c7f", bright_red="#f79b9b", bright_green="#bbe3b4",
        bright_yellow="#f7d69b", bright_blue="#adbff8", bright_magenta="#dac0f7",
        bright_cyan="#92e0d6", bright_white="#f4f5f9",
    ),
    status=dict(
        error="#f07c7c", warning="#f0c27b", info="#8fa6ee", success="#a2d39b",
        hint="#8794c4", added="#a2d39b", modified="#f0c27b", deleted="#f07c7c",
        renamed="#86c8e8", conflict="#f08fab",
    ),
    icons=dict(
        blue="#8aa5f2", sky="#7dc8ec", teal="#62cbbd", green="#9fd497",
        lime="#c6dc7e", yellow="#f2cb77", amber="#efa968", orange="#ee8d6c",
        red="#ef7676", pink="#f08fb0", purple="#bfa0f2", lavender="#a9b0f4",
        brown="#c8a17f", gray="#868b9d", cream="#e2dccd",
    ),
)

# ---------------------------------------------------------------------------
#  OBSIDIAN — near-black OLED calm. Restrained, amber-lit, Vesper-quiet.
# ---------------------------------------------------------------------------
OBSIDIAN = Variant(
    slug="obsidian",
    name="Dodo Obsidian",
    appearance="dark",
    tagline="Near-black volcanic glass, lit by a single amber ember.",
    ui=dict(
        crust="#080808",
        mantle="#0c0c0c",
        base="#111111",
        surface0="#181817",
        surface1="#201f1e",
        surface2="#2a2927",
        border="#1e1e1c",
        border_variant="#171716",
        text="#e4e1da",
        subtext="#a8a49b",
        muted="#78756e",
        faint="#4a4844",
    ),
    accent="#eda157",
    feather="#9ba7c6",
    syntax=dict(
        keyword="#eda157",
        function="#f2d8a7",
        type="#8ecfc5",
        string="#a6d6a0",
        number="#ee8f98",
        constant="#ee8f98",
        property="#b5c0e8",
        parameter="#d9c3a3",
        variable="#e4e1da",
        variable_special="#ee8f98",
        operator="#a2bfcf",
        punctuation="#6f6d67",
        bracket="#8a877f",
        comment="#64625c",
        comment_doc="#7d7a71",
        tag="#eda157",
        attribute="#f2d8a7",
        namespace="#b3ddd6",
        string_escape="#ee8f98",
        regex="#a2bfcf",
        string_special="#d9c3a3",
        heading="#eda157",
        link="#b5c0e8",
        link_uri="#8ecfc5",
        list_marker="#eda157",
        selector="#f2d8a7",
        selector_pseudo="#c9b1e6",
        literal="#a6d6a0",
        preproc="#ee8f98",
        label="#b5c0e8",
    ),
    ansi=dict(
        black="#262624", red="#ec7b6f", green="#a6d6a0", yellow="#f0c070",
        blue="#8fb0e6", magenta="#cfa3e0", cyan="#8ecfc5", white="#d5d1c9",
        bright_black="#625f59", bright_red="#f49a90", bright_green="#c0e6bb",
        bright_yellow="#f6d391", bright_blue="#adc6f0", bright_magenta="#e0bdec",
        bright_cyan="#ade0d9", bright_white="#f5f2eb",
    ),
    status=dict(
        error="#ec7b6f", warning="#eda157", info="#8fb0e6", success="#a6d6a0",
        hint="#8d97b3", added="#a6d6a0", modified="#eda157", deleted="#ec7b6f",
        renamed="#a2bfcf", conflict="#ee8f98",
    ),
    icons=dict(
        blue="#8eabe2", sky="#93c2d8", teal="#82c6bb", green="#a2cf9b",
        lime="#c2d18d", yellow="#ecc77e", amber="#eda157", orange="#e58d68",
        red="#e57a70", pink="#e696a3", purple="#c0a5de", lavender="#adb1e2",
        brown="#bf9f80", gray="#7f7c75", cream="#ddd5c4",
    ),
)

# ---------------------------------------------------------------------------
#  DAWN — warm paper light. Claude's ivory with terracotta.
# ---------------------------------------------------------------------------
DAWN = Variant(
    slug="dawn",
    name="Dodo Dawn",
    appearance="light",
    tagline="Ivory paper and terracotta at first light.",
    ui=dict(
        crust="#ebe8df",
        mantle="#f3f1ea",
        base="#faf9f5",
        surface0="#ffffff",
        surface1="#ebe8df",
        surface2="#e1ddd1",
        border="#e0dccf",
        border_variant="#ebe8df",
        text="#2a2925",
        subtext="#55524a",
        muted="#7a766c",
        faint="#aaa69b",
    ),
    accent="#c15f3c",
    feather="#5d6fa3",
    syntax=dict(
        keyword="#b5512d",
        function="#9a6408",
        type="#1c7a6e",
        string="#4b7a29",
        number="#8447be",
        constant="#8447be",
        property="#3d5ca8",
        parameter="#8c5826",
        variable="#2a2925",
        variable_special="#bb3a5b",
        operator="#2a7799",
        punctuation="#7b776c",
        bracket="#5f5c54",
        comment="#8a857a",
        comment_doc="#7d7768",
        tag="#b5512d",
        attribute="#9a6408",
        namespace="#1c7a6e",
        string_escape="#bb3a5b",
        regex="#2a7799",
        string_special="#8c5826",
        heading="#b5512d",
        link="#3d5ca8",
        link_uri="#1c7a6e",
        list_marker="#b5512d",
        selector="#9a6408",
        selector_pseudo="#8447be",
        literal="#4b7a29",
        preproc="#bb3a5b",
        label="#3d5ca8",
    ),
    ansi=dict(
        black="#3a3833", red="#c4392b", green="#4b7a29", yellow="#9a6408",
        blue="#3d5ca8", magenta="#8447be", cyan="#1c7a6e", white="#cfcabd",
        bright_black="#7a766c", bright_red="#d9573f", bright_green="#5f9636",
        bright_yellow="#b97f16", bright_blue="#5376c4", bright_magenta="#9e62d6",
        bright_cyan="#2b978a", bright_white="#e9e5da",
    ),
    status=dict(
        error="#c4392b", warning="#a8690a", info="#3d5ca8", success="#4b7a29",
        hint="#6a7aa6", added="#4b7a29", modified="#a8690a", deleted="#c4392b",
        renamed="#2a7799", conflict="#bb3a5b",
    ),
    icons=dict(
        blue="#4469c0", sky="#2d86b0", teal="#1f8a7c", green="#4f8a2e",
        lime="#7f8f1e", yellow="#a87c0c", amber="#c1720f", orange="#c45a32",
        red="#c43c31", pink="#c2486e", purple="#8a50c4", lavender="#6260c0",
        brown="#93673f", gray="#8a857a", cream="#9a8866",
    ),
)

# ---------------------------------------------------------------------------
#  MIST — cool morning fog. Grey paper with slate-feather ink.
# ---------------------------------------------------------------------------
MIST = Variant(
    slug="mist",
    name="Dodo Mist",
    appearance="light",
    tagline="Cool sea-fog grey with slate-feather ink.",
    ui=dict(
        crust="#e5e7eb",
        mantle="#eef0f3",
        base="#f7f8fa",
        surface0="#ffffff",
        surface1="#e8ebef",
        surface2="#dce0e7",
        border="#d9dde4",
        border_variant="#e6e9ee",
        text="#23262e",
        subtext="#4c5160",
        muted="#6e7486",
        faint="#a2a8b6",
    ),
    accent="#4d63b3",
    feather="#4d63b3",
    syntax=dict(
        keyword="#4a59c2",
        function="#a85a0e",
        type="#0f7882",
        string="#367a42",
        number="#b33d67",
        constant="#b33d67",
        property="#7547b3",
        parameter="#8a5b2a",
        variable="#23262e",
        variable_special="#b33d67",
        operator="#26759c",
        punctuation="#737a8b",
        bracket="#555b6b",
        comment="#828899",
        comment_doc="#737a8f",
        tag="#4a59c2",
        attribute="#a85a0e",
        namespace="#0f7882",
        string_escape="#b33d67",
        regex="#26759c",
        string_special="#8a5b2a",
        heading="#4a59c2",
        link="#7547b3",
        link_uri="#0f7882",
        list_marker="#4a59c2",
        selector="#a85a0e",
        selector_pseudo="#7547b3",
        literal="#367a42",
        preproc="#b33d67",
        label="#7547b3",
    ),
    ansi=dict(
        black="#2e323c", red="#c23a3a", green="#367a42", yellow="#9c620c",
        blue="#4a59c2", magenta="#8445b5", cyan="#0f7882", white="#cfd3db",
        bright_black="#6e7486", bright_red="#d65252", bright_green="#469656",
        bright_yellow="#bb7f1a", bright_blue="#6375d6", bright_magenta="#a061cf",
        bright_cyan="#1b96a1", bright_white="#eceef2",
    ),
    status=dict(
        error="#c23a3a", warning="#a5650c", info="#4a59c2", success="#367a42",
        hint="#6a76a8", added="#367a42", modified="#a5650c", deleted="#c23a3a",
        renamed="#26759c", conflict="#b33d67",
    ),
    icons=dict(
        blue="#4a62c4", sky="#2a83b3", teal="#13868f", green="#3c8848",
        lime="#6f8a20", yellow="#a07a0e", amber="#bc6e12", orange="#c45838",
        red="#c23e3e", pink="#bf4673", purple="#8048c0", lavender="#5d5fc6",
        brown="#8a6844", gray="#7b8192", cream="#8c826e",
    ),
)

VARIANTS: list[Variant] = [DUSK, NIGHT, OBSIDIAN, DAWN, MIST]

# Multiplayer cursors: the accent first, then the rest of the dodo, picked
# so neighbouring collaborators never share a hue family.
for _v in VARIANTS:
    s = _v.syntax
    _v.players = [
        _v.accent, s["type"], s["function"], s["number"],
        s["variable_special"], s["string"], s["operator"], s["property"],
    ]
