# Register the submod
init -990 python in mas_submod_utils:
    Submod(
        author="geneTechnician",
        name="Drink Coffee With Monika",
        description=(
            "Um submod que permite convidar a Monika para tomar um café com você!\n"
            "Está com alguma dúvida? Clique "
            "{a=https://discord.gg/vq5GZBW42R}{b}{i}aqui{/i}{/b}{/a}."
        ),
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
            user_name="MASBrasil",
            repository_name="DrinkCoffeeWithMonika-PTBR",
            submod_dir="/Submods/Drink Coffee With Monika",
            extraction_depth=3
        )