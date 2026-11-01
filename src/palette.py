"""The Dodo palette — single source of truth for every editor & terminal.

Five variants, three dark and two light. They share one idea: a quiet,
neutral grey canvas with a whisper of temperature (no heavy tint washing
over the screen), and colour that lives in the *code*, borrowed from the
dodo itself:

    feather   slate-blue plumage         → folders, properties, links
    beak      honey-gold upper bill      → functions (in every variant)
    canopy    muted island olive         → the light-mode accent
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
#  DUSK — warm graphite, lagoon-teal keywords, weathered gold calls.
# ---------------------------------------------------------------------------
DUSK = Variant(
    slug="dusk",
    name="Dodo Dusk",
    appearance="dark",
    tagline="Warm graphite and lagoon teal as the island settles.",
    ui=dict(
        crust="#1a1d1c",
        mantle="#202321",
        base="#272b29",
        surface0="#2e322f",
        surface1="#373c37",
        surface2="#42483f",
        border="#3a403a",
        border_variant="#30352f",
        text="#e4e7de",
        subtext="#b5bdb2",
        muted="#929d90",
        faint="#606b60",
    ),
    accent="#83b8a6",
    feather="#96adc8",
    syntax=dict(
        keyword="#8fc4b1",
        function="#dfbd82",
        type="#9bbfe0",
        string="#b5c98d",
        number="#c5acd9",
        constant="#c5acd9",
        property="#b0badf",
        parameter="#d4bc9b",
        variable="#e4e7de",
        variable_special="#df9fac",
        operator="#9dc6cc",
        punctuation="#98a294",
        bracket="#b0b9ac",
        comment="#929d90",
        comment_doc="#acb59e",
        tag="#8fc4b1",
        attribute="#dfbd82",
        namespace="#bad2e5",
        string_escape="#df9fac",
        regex="#9dc6cc",
        string_special="#d4bc9b",
        heading="#8fc4b1",
        link="#b0badf",
        link_uri="#9bbfe0",
        list_marker="#8fc4b1",
        selector="#dfbd82",
        selector_pseudo="#c5acd9",
        literal="#b5c98d",
        preproc="#df9fac",
        label="#b0badf",
    ),
    ansi=dict(
        black="#3a413b", red="#db8b83", green="#b5c98d", yellow="#dfbd82",
        blue="#96b4dd", magenta="#c5acd9", cyan="#83b8a6", white="#cfd6cb",
        bright_black="#929d90", bright_red="#eba59c", bright_green="#cadba8",
        bright_yellow="#efd3a0", bright_blue="#b2caec", bright_magenta="#dac3e8",
        bright_cyan="#a3d0bf", bright_white="#f2f4ec",
    ),
    status=dict(
        error="#db8b83", warning="#dfbd82", info="#96b4dd", success="#b5c98d",
        hint="#96adc8", added="#b5c98d", modified="#dfbd82", deleted="#db8b83",
        renamed="#9dc6cc", conflict="#df9fac",
    ),
    icons=dict(
        blue="#96b4dd", sky="#91c1d3", teal="#83b8a6", green="#aec78e",
        lime="#c2ce93", yellow="#dfc786", amber="#d9b078", orange="#d49b75",
        red="#db8b83", pink="#d99eae", purple="#bea5d5", lavender="#b0b4dc",
        brown="#bda486", gray="#98a294", cream="#dbd5bd",
    ),
)

# ---------------------------------------------------------------------------
#  NIGHT — deep blue slate. Moonlit feather-blue and softened beak gold.
# ---------------------------------------------------------------------------
NIGHT = Variant(
    slug="night",
    name="Dodo Night",
    appearance="dark",
    tagline="Deep blue slate and moonlit feather-blue.",
    ui=dict(
        crust="#13171d",
        mantle="#181d24",
        base="#1d222a",
        surface0="#252b34",
        surface1="#2e3540",
        surface2="#394350",
        border="#323b48",
        border_variant="#282f39",
        text="#e0e6ed",
        subtext="#b0becd",
        muted="#8d9aab",
        faint="#59697b",
    ),
    accent="#96b6e0",
    feather="#96b6e0",
    syntax=dict(
        keyword="#a0bee7",
        function="#e2bf87",
        type="#89c5bc",
        string="#a7c49a",
        number="#d9a184",
        constant="#d9a184",
        property="#bcb0db",
        parameter="#d8c4a6",
        variable="#e0e6ed",
        variable_special="#dca2ba",
        operator="#91c4d6",
        punctuation="#98a4b3",
        bracket="#afbbca",
        comment="#8d9aab",
        comment_doc="#a3b3c6",
        tag="#a0bee7",
        attribute="#e2bf87",
        namespace="#abd5cc",
        string_escape="#dca2ba",
        regex="#91c4d6",
        string_special="#d8c4a6",
        heading="#a0bee7",
        link="#bcb0db",
        link_uri="#89c5bc",
        list_marker="#a0bee7",
        selector="#e2bf87",
        selector_pseudo="#bcb0db",
        literal="#a7c49a",
        preproc="#dca2ba",
        label="#bcb0db",
    ),
    ansi=dict(
        black="#353e4b", red="#df9094", green="#a7c49a", yellow="#e2bf87",
        blue="#96b6e0", magenta="#bcb0db", cyan="#89c5bc", white="#d0dae5",
        bright_black="#8d9aab", bright_red="#eeb0b2", bright_green="#c0dbb3",
        bright_yellow="#efd5a6", bright_blue="#b5cef0", bright_magenta="#d2c5ea",
        bright_cyan="#a9ddd4", bright_white="#f1f5f9",
    ),
    status=dict(
        error="#df9094", warning="#e2bf87", info="#96b6e0", success="#a7c49a",
        hint="#9aacc8", added="#a7c49a", modified="#e2bf87", deleted="#df9094",
        renamed="#91c4d6", conflict="#dca2ba",
    ),
    icons=dict(
        blue="#96b6e0", sky="#91c4d6", teal="#89c5bc", green="#a7c49a",
        lime="#c3d39a", yellow="#e4ca8f", amber="#ddaf7c", orange="#d8a081",
        red="#df9094", pink="#dca2ba", purple="#b7a3d7", lavender="#aebae0",
        brown="#bfa78c", gray="#98a4b3", cream="#d9d6c8",
    ),
)

# ---------------------------------------------------------------------------
#  OBSIDIAN — volcanic black. Sand-gold highlights and quiet mineral hues.
# ---------------------------------------------------------------------------
OBSIDIAN = Variant(
    slug="obsidian",
    name="Dodo Obsidian",
    appearance="dark",
    tagline="Volcanic black with sand-gold highlights.",
    ui=dict(
        crust="#090b0a",
        mantle="#0e100f",
        base="#141615",
        surface0="#1b1e1b",
        surface1="#242823",
        surface2="#30352e",
        border="#282d26",
        border_variant="#1e231d",
        text="#e1e4da",
        subtext="#b0b7a8",
        muted="#858e80",
        faint="#515d4d",
    ),
    accent="#dcb575",
    feather="#a3b1c1",
    syntax=dict(
        keyword="#dcb575",
        function="#e5d2aa",
        type="#92beb8",
        string="#afc49b",
        number="#d6a0a6",
        constant="#d6a0a6",
        property="#b0bed2",
        parameter="#cbbd9f",
        variable="#e1e4da",
        variable_special="#d6a0a6",
        operator="#a1bcc5",
        punctuation="#8e9788",
        bracket="#a9b19f",
        comment="#858e80",
        comment_doc="#a1ab96",
        tag="#dcb575",
        attribute="#e5d2aa",
        namespace="#b4cec5",
        string_escape="#d6a0a6",
        regex="#a1bcc5",
        string_special="#cbbd9f",
        heading="#dcb575",
        link="#b0bed2",
        link_uri="#92beb8",
        list_marker="#dcb575",
        selector="#e5d2aa",
        selector_pseudo="#c1b1ce",
        literal="#afc49b",
        preproc="#d6a0a6",
        label="#b0bed2",
    ),
    ansi=dict(
        black="#2b3029", red="#d58f87", green="#afc49b", yellow="#dcb575",
        blue="#9eb7d5", magenta="#c1a8ce", cyan="#92beb8", white="#d0d6c7",
        bright_black="#858e80", bright_red="#e7aaa2", bright_green="#c7d8b3",
        bright_yellow="#ecd1a2", bright_blue="#bacedf", bright_magenta="#d7c0df",
        bright_cyan="#b0d4cc", bright_white="#f1f4e9",
    ),
    status=dict(
        error="#d58f87", warning="#dcb575", info="#9eb7d5", success="#afc49b",
        hint="#a3b1c1", added="#afc49b", modified="#dcb575", deleted="#d58f87",
        renamed="#a1bcc5", conflict="#d6a0a6",
    ),
    icons=dict(
        blue="#9eb7d5", sky="#a1bcc5", teal="#92beb8", green="#afc49b",
        lime="#c4cb9f", yellow="#dfca91", amber="#dcb575", orange="#cda17e",
        red="#d58f87", pink="#d6a0a6", purple="#bca9cc", lavender="#b1bacf",
        brown="#b5a88b", gray="#8e9788", cream="#d9d6bf",
    ),
)

# ---------------------------------------------------------------------------
#  DAWN — pale limestone. Olive ink and weathered brass at first light.
# ---------------------------------------------------------------------------
DAWN = Variant(
    slug="dawn",
    name="Dodo Dawn",
    appearance="light",
    tagline="Pale limestone and olive ink at first light.",
    ui=dict(
        crust="#e5e3da",
        mantle="#eeece3",
        base="#f6f4ed",
        surface0="#ffffff",
        surface1="#e7e8dc",
        surface2="#dcdfcf",
        border="#d4d9c8",
        border_variant="#e3e5d8",
        text="#2c3029",
        subtext="#50594a",
        muted="#687160",
        faint="#a2aa96",
    ),
    accent="#5e7447",
    feather="#58718f",
    syntax=dict(
        keyword="#5e7447",
        function="#8d681e",
        type="#347479",
        string="#537341",
        number="#815e9e",
        constant="#815e9e",
        property="#4e6792",
        parameter="#865d36",
        variable="#2c3029",
        variable_special="#a34f66",
        operator="#3d7390",
        punctuation="#6b7264",
        bracket="#56604d",
        comment="#687160",
        comment_doc="#606d55",
        tag="#5e7447",
        attribute="#8d681e",
        namespace="#347479",
        string_escape="#a34f66",
        regex="#3d7390",
        string_special="#865d36",
        heading="#5e7447",
        link="#4e6792",
        link_uri="#347479",
        list_marker="#5e7447",
        selector="#8d681e",
        selector_pseudo="#815e9e",
        literal="#537341",
        preproc="#a34f66",
        label="#4e6792",
    ),
    ansi=dict(
        black="#353d30", red="#b54e43", green="#537341", yellow="#8d681e",
        blue="#4e6792", magenta="#815e9e", cyan="#347479", white="#cbd0bf",
        bright_black="#687160", bright_red="#bd5549", bright_green="#5a7948",
        bright_yellow="#906d22", bright_blue="#547197", bright_magenta="#8b669e",
        bright_cyan="#3b7b79", bright_white="#e8ebdf",
    ),
    status=dict(
        error="#b54e43", warning="#8d681e", info="#4e6792", success="#537341",
        hint="#58718f", added="#537341", modified="#8d681e", deleted="#b54e43",
        renamed="#3d7390", conflict="#a34f66",
    ),
    icons=dict(
        blue="#4e6792", sky="#39788e", teal="#347479", green="#537341",
        lime="#6d782f", yellow="#8d721f", amber="#916927", orange="#a36440",
        red="#b54e43", pink="#a34f66", purple="#815e9e", lavender="#65699b",
        brown="#865d36", gray="#687160", cream="#82754f",
    ),
)

# ---------------------------------------------------------------------------
#  MIST — sea-fog grey. Blue-grey ink and restrained coastal hues.
# ---------------------------------------------------------------------------
MIST = Variant(
    slug="mist",
    name="Dodo Mist",
    appearance="light",
    tagline="Sea-fog grey with blue-grey coastal ink.",
    ui=dict(
        crust="#dfe6e8",
        mantle="#e9eff0",
        base="#f2f5f6",
        surface0="#ffffff",
        surface1="#e1e9ec",
        surface2="#d4e0e5",
        border="#ccdbe0",
        border_variant="#dde7ea",
        text="#29323a",
        subtext="#4d5e6a",
        muted="#65717b",
        faint="#9cabb3",
    ),
    accent="#4b7088",
    feather="#4b7088",
    syntax=dict(
        keyword="#4b7088",
        function="#966627",
        type="#2a7775",
        string="#47734e",
        number="#9a4e70",
        constant="#9a4e70",
        property="#705d9c",
        parameter="#825f3a",
        variable="#29323a",
        variable_special="#9a4e70",
        operator="#3b728b",
        punctuation="#65717b",
        bracket="#526571",
        comment="#65717b",
        comment_doc="#596e7d",
        tag="#4b7088",
        attribute="#966627",
        namespace="#2a7775",
        string_escape="#9a4e70",
        regex="#3b728b",
        string_special="#825f3a",
        heading="#4b7088",
        link="#705d9c",
        link_uri="#2a7775",
        list_marker="#4b7088",
        selector="#966627",
        selector_pseudo="#705d9c",
        literal="#47734e",
        preproc="#9a4e70",
        label="#705d9c",
    ),
    ansi=dict(
        black="#303e48", red="#b44f51", green="#47734e", yellow="#966627",
        blue="#4b7088", magenta="#835d9d", cyan="#2a7775", white="#c7d3d9",
        bright_black="#65717b", bright_red="#ba5559", bright_green="#4f7a56",
        bright_yellow="#977027", bright_blue="#53778e", bright_magenta="#8c659e",
        bright_cyan="#317e7b", bright_white="#e5edf0",
    ),
    status=dict(
        error="#b44f51", warning="#966627", info="#4b7088", success="#47734e",
        hint="#596f89", added="#47734e", modified="#966627", deleted="#b44f51",
        renamed="#3b728b", conflict="#9a4e70",
    ),
    icons=dict(
        blue="#4b7088", sky="#36778d", teal="#2a7775", green="#47734e",
        lime="#667b37", yellow="#927222", amber="#9b6c27", orange="#a56342",
        red="#b44f51", pink="#9a4e70", purple="#705d9c", lavender="#626e9e",
        brown="#825f3a", gray="#65717b", cream="#80785b",
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
