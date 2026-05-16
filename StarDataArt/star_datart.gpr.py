register(
    TOOL,
    id="Star Data Art",
    name=_("Star Data Art"),
    description=_("Generates a spiral visualization of all family members as colored stars"),
    version="1.0.0",
    gramps_target_version="6.0",
    status=STABLE,
    fname="star_datart.py",
    toolclass="StarDatArtTool",
    optionclass="StarDatArtOptions",
    tool_modes=[TOOL_MODE_GUI],
    category=TOOL_UTILS,
)
