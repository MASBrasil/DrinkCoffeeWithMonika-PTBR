init python:

    gt_acs_playermug = MASAccessory(
        "player_mug",
        "player_mug",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        keep_on_desk=True
    )
    store.mas_sprites.init_acs(gt_acs_playermug)

default -5 persistent._player_likes_coffee = True
default -5 persistent._coffee_pref = None
default -5 persistent._drink_pref_hot = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_drink_coffee",
            category=["nós"],
            prompt="Gostaria de tomar um café comigo?",
            conditional="mas_consumable_coffee.enabled()",
            pool=True,
            aff_range=(mas_aff.HAPPY, None),
            rules={"no_unlock": None},
            action=EV_ACT_UNLOCK
        ),
    )

label monika_drink_coffee:

    if not mas_globals.time_of_day_4state == "night":
        if MASConsumable._getCurrentDrink() == mas_consumable_coffee:
            $ persistent._has_coffee = True
            $ persistent._has_prepared = True
            m 1hua "Claro, eu adoraria tomar café com você."
            if monika_chr.is_wearing_acs(mas_acs_mug):
                m 3eub "Já preparei um aqui, então você deveria fazer um café para você também, se ainda não tiver feito."
            else:
                m 3eub "Estou preparando o café agora, então pode aproveitar e fazer o seu também."
            if persistent.seen_playermug:
                m 3eua "Vou pegar a sua xícara para você.{w=0.5}{nw}"
                jump drink_with_monika
            else:
                pass

        elif MASConsumable._getCurrentDrink() == mas_consumable_hotchocolate:
            if monika_chr.is_wearing_acs(mas_acs_hotchoc_mug):
                m 1eud "Eu diria que sim, mas já estou tomando um chocolate quente."
            else:
                m 1eud "Eu diria que sim, mas já comecei a preparar um chocolate quente."
            m 3eub "Se você quiser, pode preparar um também para tomarmos [ju]."
            m 1hua "Não se preocupe, [player], da próxima vez vamos tomar café [juh]~"

        else:
            if persistent.amount_of_coffees > 0:
                if datetime.datetime.now() > persistent.amount_of_coffees_time + datetime.timedelta(hours=9):
                    jump drink_coffee_refresh

                else:
                    if persistent.amount_of_coffees >= 5:
                        m 2eksdla "Acho que já tomamos café suficiente por hoje, [mas_get_player_nickname()]."
                        m 7mksdla "Não me leve a mal,{w=0.5} eu adoro café,{w=0.5} mas exagerar pode acabar sendo ruim."
                        m 4hkb "Acho que é verdade o que dizem:{w=0.3} até coisas boas {i}podem{/i} ser demais, ahaha!"
                        m 1eka "Não se preocupe, [player], adoraria tomar um café com você de novo amanhã~"

                    else:
                        $ persistent._has_prepared = True
                        $ persistent._has_coffee = False

                        m 1etu "Quer tomar {i}outra{/i} xícara comigo?"
                        if mas_globals.time_of_day_4state == "evening":
                            m 7lud "Tudo bem, mas lembre que já está tarde, então acho melhor não tomarmos mais depois disso."
                            m 7eua "Vou preparar outra rodada para nós.{w=1}{nw}"
                            $ persistent.amount_of_coffees = 5
                        else:
                            if persistent.amount_of_coffees == 4:
                                m 4mub "Uau,{w=0.5} você parece gostar de café até mais do que eu..."
                            m 7hub "Tá bom, tá bom, vou preparar outra rodada para nós~ Ahaha!{w=1}{nw}"

                        jump drink_with_monika

            else:
                jump drink_coffee_refresh

    else:
        if MASConsumable._getCurrentDrink() == mas_consumable_coffee:
            if monika_chr.is_wearing_acs(mas_acs_mug):
                mm 1gssdlb "Eu até aceitaria, mas gostaria de terminar minha xícara antes que fique tarde."
            else:
                m 1gssdlb "Eu até aceitaria, mas preciso terminar de tomar o café que estou preparando antes que fique tarde."
            m 1eka "Não se preocupe, [player], vamos tomar um café [ju] amanhã~"

        else:
            m 1rksdla "Eu diria que sim, mas...{w=0.5}{nw}"
            extend 3ekd " já está bem tarde, [player]."
            m 4eud "Tomar café antes de dormir atrapalha o sono, e noites mal dormidas podem afetar bastante a sua saúde."
            m 7eub "Que tal tomar um chá em vez disso?"
            m 3eua "Uma xícara de chá antes de dormir pode ser super relaxante,{w=0.3} e até ajuda a aliviar o estresse e a ansiedade."
            m 1eksdla "Infelizmente, não tenho nada para preparar chá aqui, então você vai ter que tomar sem mim."
return

label drink_coffee_refresh:

    m 1sub "Claro!"
    if mas_globals.time_of_day_4state == "evening":
        m 7lud "Só lembrando que já está bem tarde... então acho melhor não tomarmos muito café."
        $ persistent.amount_of_coffees = 4
    else:
        m 3eub "Nunca perco a oportunidade de tomar um delicioso café."
        m 1hublu "Principalmente se posso compartilhá-lo com você, [mas_get_player_nickname()]~"

        $ persistent.amount_of_coffees = 0
    m 7eua "Você já preparou seu café?"

    $ _history_list.pop()
    menu:
        m "Você já preparou seu café?{fast}"

        "Sim.":
            $ persistent._has_prepared = True
            $ persistent._has_coffee = False
            m 1wuo "Acho que devo fazer um para mim antes que o seu esfrie!"
            m 2eub "Já volto rapidinho.{w=1}{nw}"

        "Ainda não.":
            $ persistent._has_prepared = False
            $ persistent._has_coffee = False
            m 1eub "Então vamos aproveitar e preparar nosso café [ju]."
            m 3eua "Volto em alguns minutos, você pode fazer o seu ao mesmo tempo."
            if mas_getSessionLength() >= datetime.timedelta(hours=2):
                m 4eub "Aproveite também para esticar um pouco as pernas."
            m 2euu "Tente não sentir tanta falta de mim...{w=1}{nw}"

    jump drink_with_monika
return

label drink_with_monika:

    call mas_transition_to_emptydesk
    if persistent._has_prepared == True:
        pause 5.0
    else:
        pause 120.0
    call mas_transition_from_emptydesk
    if persistent._has_coffee == False:
        $ mas_consumable_coffee.prepare()
    else:
        pass
    $ monika_chr.wear_acs(gt_acs_playermug)

    if persistent._has_coffee == True:
        m 1eua "Pronto~"
        m 1eub "Me avise quando terminar seu café, tudo bem?"

    elif persistent._has_prepared == True:
        m 3eub "Tudo certo, está preparando agora e deve ficar pronto em alguns minutos."
        if not persistent.seen_playermug:
            m 1rkblsdla ".{w=0.5}.{w=0.5}."
            m 3rkblsdlb "Como pode ver, coloquei uma xícara extra na mesa."
            m 2ekbfa "Pensei que assim ficaria mais como se estivéssemos tomando nosso café [ju]."
            m 7hkbfsdlb "Espero que não soe brega demais..."
            m 1mkbfa "Enfim..."
            $ persistent.seen_playermug = True
        else:
            pass
        m 1eub "Me avise quando terminar seu café, tá?"

    else:
        m 1eub "Voltei~{w=1}{nw}"
        m 3eua "Você também pode apertar a opção na tela para me avisar quando voltar.{nw}"

        $ _history_list.pop()
        menu:
            m "Você também pode apertar a opção na tela para me avisar quando voltar.{fast}"

            "Voltei!":
                m 1hub "Bem-[vn] de volta, [mas_get_player_nickname()]~"
                if not persistent.seen_playermug:
                    m 1rkblsdla ".{w=0.5}.{w=0.5}."
                    m 3rkblsdlb "Como pode ver, coloquei uma xícara extra na mesa."
                    m 2ekbfa "Pensei que assim ficaria mais como se estivéssemos tomando nosso café [ju]."
                    m 7hkbfsdlb "Espero que não soe brega demais..."
                    m 1mkbfa "Enfim..."
                    $ persistent.seen_playermug = True
                else:
                    pass
                m 3eub "Meu café ficou pronto enquanto você estava fora, então deve estar quase na temperatura certa."
                m 1eub "Me avise quando terminar o seu, tá?"

    $ persistent._is_drinking_coffee = True

    $ mas_idle_mailbox.send_idle_cb("drink_together_callback")
return "idle"

label drink_together_callback:
    $ mas_gainAffection(3, bypass=False)

    if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=5), "monika_drink_coffee"):
        m 1eub "Já terminou seu café, [mas_get_player_nickname()]?"
    else:
        m 2wuo "Uau, você bebeu rápido demais!"
        m 1lka "Espero que não tenha queimado a língua..."
    m 3eua "Vou guardar minha xícara."
    if MASConsumable._getCurrentDrink() == mas_consumable_coffee:
        m "Ainda não terminei meu café, então vou guardar minha xícara para mais tarde."
    $ monika_chr.remove_acs(gt_acs_playermug)
    call mas_transition_to_emptydesk
    pause 5.0
    call mas_transition_from_emptydesk
    m 1hua "Voltei~"
    m 1ekbsu "Obrigada por querer passar esse tempinho comigo~"

    $ persistent.amount_of_coffees += 1
    $ persistent.amount_of_coffees_time = datetime.datetime.now()

    $ persistent._is_drinking_coffee = False
return