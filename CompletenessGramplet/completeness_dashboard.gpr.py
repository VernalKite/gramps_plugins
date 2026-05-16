register(
    GRAMPLET,
    id="Data Completeness Dashboard",
    name=_("Data Completeness Dashboard"),
    description=_("Shows missing data statistics and a list of the most incomplete persons"),
    version="1.0.0",
    gramps_target_version="6.0",
    status=STABLE,
    fname="completeness_dashboard.py",
    height=300,
    expand=True,
    gramplet="CompletenessGramplet",
    gramplet_title=_("Completeness"),
)
