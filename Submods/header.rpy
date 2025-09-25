# Register the submod
init -990 python in mas_submod_utils:
    Submod(
        author="geneTechnician",
        name="Drink coffee with Monika",
        description="A submod that let's you ask Monika if she will drink some coffee with you!",
        version="1.1.1",
        dependencies={},
        settings_pane=None,
        version_updates={}
    )

# Register the updater
init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Drink coffee with Monika",
            user_name="geneTechnician",
            repository_name="drink-coffee-with-monika",
            submod_dir="/Submods/Drink Coffee With Monika",
            extraction_depth=3
        )

