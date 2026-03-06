# Gardenlog Tests by Antigravity

## Test run output

```
❯ python manage.py test -v2
Found 105 test(s).
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Operations to perform:
  Synchronize unmigrated apps: messages, staticfiles
  Apply all migrations: admin, auth, contenttypes, garden, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying garden.0001_initial... OK
  Applying garden.0002_category_plantspecies_category_link... OK
  Applying garden.0003_auto_20260228_0935... OK
  Applying garden.0004_remove_plantspecies_category_link_and_more... OK
  Applying sessions.0001_initial... OK
System check identified no issues (0 silenced).
test_str (garden.tests.GardenNoteModelTest.test_str)
Varmistaa, että havainnon tekstiesitys katkaisee pitkän tekstin. ... ok
test_itamisaika_max_pv_float_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_itamisaika_max_pv_float_invalid)
itamisaika_max_pv='3.5' ei ole sallittu kokonaislukukentälle. ... ok
test_itamisaika_max_pv_string_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_itamisaika_max_pv_string_invalid)
itamisaika_max_pv='foobar' ei ole sallittu. ... ok
test_itamisaika_min_pv_float_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_itamisaika_min_pv_float_invalid)
itamisaika_min_pv='3.5' ei ole sallittu kokonaislukukentälle. ... ok
test_itamisaika_min_pv_string_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_itamisaika_min_pv_string_invalid)
itamisaika_min_pv='foobar' ei ole sallittu. ... ok
test_korkeus_cm_blank_valid (garden.tests.LomakeNumeerisetVirheellisetTest.test_korkeus_cm_blank_valid)
korkeus_cm voidaan jättää tyhjäksi (nullable). ... ok
test_korkeus_cm_float_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_korkeus_cm_float_invalid)
korkeus_cm='50.5' ei ole sallittu kokonaislukukentälle. ... ok
test_korkeus_cm_negative_valid_model_level (garden.tests.LomakeNumeerisetVirheellisetTest.test_korkeus_cm_negative_valid_model_level)
korkeus_cm hyväksyy negatiivisen arvon mallin tasolla (ei lomakerajoitetta). ... ok
test_korkeus_cm_string_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_korkeus_cm_string_invalid)
korkeus_cm='foobar' ei ole sallittu. ... ok
test_kylvo_alku_kk_12_valid (garden.tests.LomakeNumeerisetVirheellisetTest.test_kylvo_alku_kk_12_valid)
kylvo_alku_kk=12 on sallittu maksimiarvo. ... ok
test_kylvo_alku_kk_13_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_kylvo_alku_kk_13_invalid)
kylvo_alku_kk=13 ei ole sallittu valinta. ... ok
test_kylvo_alku_kk_1_valid (garden.tests.LomakeNumeerisetVirheellisetTest.test_kylvo_alku_kk_1_valid)
kylvo_alku_kk=1 on sallittu minimiarvo. ... ok
test_kylvo_alku_kk_float_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_kylvo_alku_kk_float_invalid)
kylvo_alku_kk='3.5' ei ole sallittu valinta. ... ok
test_kylvo_alku_kk_negative_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_kylvo_alku_kk_negative_invalid)
kylvo_alku_kk=-1 ei ole sallittu valinta. ... ok
test_kylvo_alku_kk_string_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_kylvo_alku_kk_string_invalid)
kylvo_alku_kk='foobar' ei ole sallittu valinta. ... ok
test_kylvo_alku_kk_zero_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_kylvo_alku_kk_zero_invalid)
kylvo_alku_kk=0 ei ole sallittu valinta. ... ok
test_kylvo_loppu_kk_13_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_kylvo_loppu_kk_13_invalid)
kylvo_loppu_kk=13 ei ole sallittu valinta. ... ok
test_kylvo_loppu_kk_string_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_kylvo_loppu_kk_string_invalid)
kylvo_loppu_kk='foobar' ei ole sallittu valinta. ... ok
test_kylvo_loppu_kk_zero_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_kylvo_loppu_kk_zero_invalid)
kylvo_loppu_kk=0 ei ole sallittu valinta. ... ok
test_sato_alku_kk_13_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_sato_alku_kk_13_invalid)
sato_alku_kk=13 ei ole sallittu valinta. ... ok
test_sato_alku_kk_negative_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_sato_alku_kk_negative_invalid)
sato_alku_kk=-1 ei ole sallittu valinta. ... ok
test_sato_alku_kk_string_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_sato_alku_kk_string_invalid)
sato_alku_kk='foobar' ei ole sallittu valinta. ... ok
test_sato_alku_kk_zero_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_sato_alku_kk_zero_invalid)
sato_alku_kk=0 ei ole sallittu valinta. ... ok
test_sato_loppu_kk_12_valid (garden.tests.LomakeNumeerisetVirheellisetTest.test_sato_loppu_kk_12_valid)
sato_loppu_kk=12 on sallittu maksimiarvo. ... ok
test_sato_loppu_kk_13_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_sato_loppu_kk_13_invalid)
sato_loppu_kk=13 ei ole sallittu valinta. ... ok
test_sato_loppu_kk_1_valid (garden.tests.LomakeNumeerisetVirheellisetTest.test_sato_loppu_kk_1_valid)
sato_loppu_kk=1 on sallittu minimiarvo. ... ok
test_sato_loppu_kk_negative_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_sato_loppu_kk_negative_invalid)
sato_loppu_kk=-1 ei ole sallittu valinta. ... ok
test_sato_loppu_kk_string_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_sato_loppu_kk_string_invalid)
sato_loppu_kk='foobar' ei ole sallittu valinta. ... ok
test_sato_loppu_kk_zero_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_sato_loppu_kk_zero_invalid)
sato_loppu_kk=0 ei ole sallittu valinta. ... ok
test_siemenia_blank_valid (garden.tests.LomakeNumeerisetVirheellisetTest.test_siemenia_blank_valid)
siemenia_pakkauksessa voidaan jättää tyhjäksi (nullable). ... ok
test_siemenia_float_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_siemenia_float_invalid)
siemenia_pakkauksessa='3.5' ei ole sallittu kokonaislukukentälle. ... ok
test_siemenia_string_invalid (garden.tests.LomakeNumeerisetVirheellisetTest.test_siemenia_string_invalid)
siemenia_pakkauksessa='foobar' ei ole sallittu. ... ok
test_kasvupaikka_empty_invalid (garden.tests.LomakeVirheellisetValinnatTest.test_kasvupaikka_empty_invalid)
PlantSpeciesForm hylkää tyhjän kasvupaikka-arvon. ... ok
test_kasvupaikka_invalid_choice (garden.tests.LomakeVirheellisetValinnatTest.test_kasvupaikka_invalid_choice)
PlantSpeciesForm hylkää tuntemattoman kasvupaikka-arvon. ... ok
test_kasvupaikka_valid_all_choices (garden.tests.LomakeVirheellisetValinnatTest.test_kasvupaikka_valid_all_choices)
PlantSpeciesForm hyväksyy kaikki kelvolliset kasvupaikka-vaihtoehdot. ... ok
test_tila_empty_choice_invalid (garden.tests.LomakeVirheellisetValinnatTest.test_tila_empty_choice_invalid)
TilaForm hylkää tyhjän tila-arvon. ... ok
test_tila_invalid_choice (garden.tests.LomakeVirheellisetValinnatTest.test_tila_invalid_choice)
TilaForm hylkää tuntemattoman tila-arvon. ... ok
test_tila_numeric_invalid (garden.tests.LomakeVirheellisetValinnatTest.test_tila_numeric_invalid)
TilaForm hylkää numeerisen tila-arvon. ... ok
test_tila_valid_all_choices (garden.tests.LomakeVirheellisetValinnatTest.test_tila_valid_all_choices)
TilaForm hyväksyy kaikki kelvolliset tila-vaihtoehdot. ... ok
test_category_name_arabic (garden.tests.MultibyteTekstitTest.test_category_name_arabic)
Kategoria voidaan luoda arabiankielisellä nimellä. ... ok
test_category_name_chinese (garden.tests.MultibyteTekstitTest.test_category_name_chinese)
Kategoria voidaan luoda kiinalaisin merkein. ... ok
test_category_name_emoji (garden.tests.MultibyteTekstitTest.test_category_name_emoji)
Kategoria voidaan luoda emoji-nimellä. ... ok
test_mygarden_kasvupaikka_arabic (garden.tests.MultibyteTekstitTest.test_mygarden_kasvupaikka_arabic)
Viljelymerkinnän kasvupaikka hyväksyy arabialaisen tekstin. ... ok
test_mygarden_kasvupaikka_chinese (garden.tests.MultibyteTekstitTest.test_mygarden_kasvupaikka_chinese)
Viljelymerkinnän kasvupaikka hyväksyy kiinalaiset merkit. ... ok
test_mygarden_kasvupaikka_emoji (garden.tests.MultibyteTekstitTest.test_mygarden_kasvupaikka_emoji)
Viljelymerkinnän kasvupaikka hyväksyy emojit. ... ok
test_mygarden_muistiinpanot_arabic (garden.tests.MultibyteTekstitTest.test_mygarden_muistiinpanot_arabic)
Muistiinpanot-kenttä hyväksyy arabialaisen tekstin. ... ok
test_mygarden_muistiinpanot_chinese (garden.tests.MultibyteTekstitTest.test_mygarden_muistiinpanot_chinese)
Muistiinpanot-kenttä hyväksyy kiinalaiset merkit. ... ok
test_mygarden_muistiinpanot_emoji (garden.tests.MultibyteTekstitTest.test_mygarden_muistiinpanot_emoji)
Muistiinpanot-kenttä hyväksyy emojit. ... ok
test_mygarden_muistiinpanot_mixed (garden.tests.MultibyteTekstitTest.test_mygarden_muistiinpanot_mixed)
Muistiinpanot-kenttä hyväksyy sekakielisen tekstin. ... ok
test_note_havainto_arabic (garden.tests.MultibyteTekstitTest.test_note_havainto_arabic)
Havainnon teksti hyväksyy arabialaisen tekstin. ... ok
test_note_havainto_chinese (garden.tests.MultibyteTekstitTest.test_note_havainto_chinese)
Havainnon teksti hyväksyy kiinalaiset merkit. ... ok
test_note_havainto_emoji (garden.tests.MultibyteTekstitTest.test_note_havainto_emoji)
Havainnon teksti hyväksyy emojit. ... ok
test_plant_kasvatusohje_arabic (garden.tests.MultibyteTekstitTest.test_plant_kasvatusohje_arabic)
Kasvatusohje-kenttä hyväksyy arabialaisen tekstin. ... ok
test_plant_kuvaus_mixed_scripts (garden.tests.MultibyteTekstitTest.test_plant_kuvaus_mixed_scripts)
Kuvaus-kenttä hyväksyy sekakielisen tekstin (emoji + arabia + kiina). ... ok
test_plant_lajike_arabic (garden.tests.MultibyteTekstitTest.test_plant_lajike_arabic)
Kasvilajin lajike voidaan tallentaa arabiankielisellä tekstillä. ... ok
test_plant_lajike_chinese (garden.tests.MultibyteTekstitTest.test_plant_lajike_chinese)
Kasvilajin lajike voidaan tallentaa kiinalaisilla merkeillä. ... ok
test_plant_nelson_garden_id_chinese (garden.tests.MultibyteTekstitTest.test_plant_nelson_garden_id_chinese)
Nelson Garden ID -kenttä hyväksyy kiinalaiset merkit. ... ok
test_plant_nimi_arabic (garden.tests.MultibyteTekstitTest.test_plant_nimi_arabic)
Kasvilajin nimi voidaan tallentaa arabiankielisellä tekstillä. ... ok
test_plant_nimi_chinese (garden.tests.MultibyteTekstitTest.test_plant_nimi_chinese)
Kasvilajin nimi voidaan tallentaa kiinalaisilla merkeillä. ... ok
test_plant_nimi_emoji (garden.tests.MultibyteTekstitTest.test_plant_nimi_emoji)
Kasvilajin nimi voidaan tallentaa emojein. ... ok
test_arvioitu_sato (garden.tests.MyGardenModelTest.test_arvioitu_sato)
Varmistaa, että arvioitu sato lasketaan oikein kylvöpäivän perusteella. ... ok
test_arvioitu_sato_ilman_kylvopaivaa (garden.tests.MyGardenModelTest.test_arvioitu_sato_ilman_kylvopaivaa)
Varmistaa, että arvioitu sato on None, jos kylvöpäivää ei ole määritelty. ... ok
test_str (garden.tests.MyGardenModelTest.test_str)
Varmistaa, että viljelymerkinnän tekstiesitys sisältää kasvin nimen. ... ok
test_mygarden_kasvupaikka_newline (garden.tests.OhjausmerkkiTest.test_mygarden_kasvupaikka_newline)
Kasvupaikka hyväksyy rivinvaihdon. ... ok
test_mygarden_kasvupaikka_tab (garden.tests.OhjausmerkkiTest.test_mygarden_kasvupaikka_tab)
Kasvupaikka hyväksyy tabulaattorin. ... ok
test_mygarden_muistiinpanot_control_chars (garden.tests.OhjausmerkkiTest.test_mygarden_muistiinpanot_control_chars)
Muistiinpanot hyväksyy ohjausmerkit (\x01, \x1f, \x7f). ... ok
test_note_havainto_control_chars (garden.tests.OhjausmerkkiTest.test_note_havainto_control_chars)
Havainto hyväksyy ohjausmerkit. ... ok
test_note_havainto_del_char (garden.tests.OhjausmerkkiTest.test_note_havainto_del_char)
Havainto hyväksyy DEL-merkin (\x7f). ... ok
test_plant_kasvatusohje_null_byte (garden.tests.OhjausmerkkiTest.test_plant_kasvatusohje_null_byte)
Kasvatusohje hyväksyy null-tavun sisältävän merkkijonon. ... ok
test_plant_kuvaus_carriage_return (garden.tests.OhjausmerkkiTest.test_plant_kuvaus_carriage_return)
Kuvaus hyväksyy Windows-tyylisen rivinvaihdon (\r\n). ... ok
test_plant_kuvaus_newlines_and_tabs (garden.tests.OhjausmerkkiTest.test_plant_kuvaus_newlines_and_tabs)
Kuvaus hyväksyy rivinvaihdot ja tabulaattorit. ... ok
test_plant_kuvaus_unicode_control_chars (garden.tests.OhjausmerkkiTest.test_plant_kuvaus_unicode_control_chars)
Kuvaus hyväksyy Unicode-ohjausmerkit (U+0001–U+001F). ... ok
test_category_name_long_boundary (garden.tests.PitkaTekstitTest.test_category_name_long_boundary)
Kategorian nimi hyväksyy 50 merkin pituuden (max_length raja). ... ok
test_mygarden_muistiinpanot_very_long (garden.tests.PitkaTekstitTest.test_mygarden_muistiinpanot_very_long)
Muistiinpanot-tekstikenttä hyväksyy erittäin pitkän tekstin (100 000 merkkiä). ... ok
test_note_havainto_very_long (garden.tests.PitkaTekstitTest.test_note_havainto_very_long)
GardenNote-havainto hyväksyy erittäin pitkän tekstin (100 000 merkkiä). ... ok
test_note_str_truncates_at_50_chars (garden.tests.PitkaTekstitTest.test_note_str_truncates_at_50_chars)
GardenNote __str__ katkaisee havainnon 50 merkin jälkeen. ... ok
test_plant_kasvatusohje_very_long (garden.tests.PitkaTekstitTest.test_plant_kasvatusohje_very_long)
Kasvatusohje-tekstikenttä hyväksyy erittäin pitkän tekstin (100 000 merkkiä). ... ok
test_plant_kuvaus_very_long (garden.tests.PitkaTekstitTest.test_plant_kuvaus_very_long)
Kuvaus-tekstikenttä hyväksyy erittäin pitkän tekstin (100 000 merkkiä). ... ok
test_kylvo_kuukaudet (garden.tests.PlantSpeciesModelTest.test_kylvo_kuukaudet)
Varmistaa, että kylvökuukaudet palautetaan oikeana listana. ... ok
test_sato_kuukaudet (garden.tests.PlantSpeciesModelTest.test_sato_kuukaudet)
Varmistaa, että satokuukaudet palautetaan oikeana listana. ... ok
test_str (garden.tests.PlantSpeciesModelTest.test_str)
Varmistaa, että tekstiesitys sisältää nimen ja lajikkeen. ... ok
test_str_ilman_lajiketta (garden.tests.PlantSpeciesModelTest.test_str_ilman_lajiketta)
Varmistaa, että tekstiesitys toimii pelkällä nimellä, jos lajiketta ei ole. ... ok
test_etusivu (garden.tests.ViewsTest.test_etusivu)
Testaa etusivun latautumisen ja sisällön vastaavuuden. ... ok
test_kasvilista (garden.tests.ViewsTest.test_kasvilista)
Testaa kasvilistan latautumisen ja kasvien näkymisen listalla. ... ok
test_kasvilista_suodatus (garden.tests.ViewsTest.test_kasvilista_suodatus)
Testaa kasvilistan suodattamisen kategorialla. ... ok
test_lisaa_havainto (garden.tests.ViewsTest.test_lisaa_havainto)
Testaa uuden havainnon liittämisen viljelymerkintään. ... ok
test_lisaa_kasvilaji (garden.tests.ViewsTest.test_lisaa_kasvilaji)
Testaa uuden kasvilajin lisäämislomakkeen latautumisen. ... ok
test_lisaa_viljely (garden.tests.ViewsTest.test_lisaa_viljely)
Testaa uuden viljelymerkinnän lisäämislomakkeen latautumisen. ... ok
test_lisaa_viljely_post (garden.tests.ViewsTest.test_lisaa_viljely_post)
Testaa tallennuksen onnistumisen uuden viljelymerkinnän luomisessa. ... ok
test_vaihda_tila (garden.tests.ViewsTest.test_vaihda_tila)
Testaa viljelymerkinnän tilan muuttamisen tallentumisen. ... ok
test_viljely_detail (garden.tests.ViewsTest.test_viljely_detail)
Testaa viljelymerkinnän tiedot -sivun latautumisen. ... ok
test_cascade_delete_category_removes_plants (garden.tests.VirheellisetAssosiaatiotTest.test_cascade_delete_category_removes_plants)
Kategorian poistaminen poistaa kaikki siihen liittyvät kasvilajit. ... ok
test_cascade_delete_plant_removes_viljelyt (garden.tests.VirheellisetAssosiaatiotTest.test_cascade_delete_plant_removes_viljelyt)
Kasvilajin poistaminen poistaa kaikki siihen liittyvät viljelymerkinnät. ... ok
test_cascade_delete_viljely_removes_notes (garden.tests.VirheellisetAssosiaatiotTest.test_cascade_delete_viljely_removes_notes)
Viljelymerkinnän poistaminen poistaa kaikki siihen liittyvät havainnot. ... ok
test_category_name_unique (garden.tests.VirheellisetAssosiaatiotTest.test_category_name_unique)
Kategorian nimi on yksilöllinen — duplikaatin luominen heittää poikkeuksen. ... ok
test_gardennote_invalid_kasvi_ref (garden.tests.VirheellisetAssosiaatiotTest.test_gardennote_invalid_kasvi_ref)
GardenNote ei voi viitata olemattomaan MyGarden-merkintään (sovellustason tarkistus). ... ok
test_mygarden_form_missing_kasvilaji (garden.tests.VirheellisetAssosiaatiotTest.test_mygarden_form_missing_kasvilaji)
MyGardenForm hylkää puuttuvan kasvilaji-kentän. ... ok
test_mygarden_form_nonexistent_kasvilaji (garden.tests.VirheellisetAssosiaatiotTest.test_mygarden_form_nonexistent_kasvilaji)
MyGardenForm hylkää olemattoman kasvilaji-id:n. ... ok
test_mygarden_form_string_kasvilaji (garden.tests.VirheellisetAssosiaatiotTest.test_mygarden_form_string_kasvilaji)
MyGardenForm hylkää merkkijonon kasvilaji-kentässä. ... ok
test_plant_form_missing_category (garden.tests.VirheellisetAssosiaatiotTest.test_plant_form_missing_category)
PlantSpeciesForm hylkää puuttuvan kategoria-kentän. ... ok
test_plant_form_nonexistent_category (garden.tests.VirheellisetAssosiaatiotTest.test_plant_form_nonexistent_category)
PlantSpeciesForm hylkää olemattoman kategoria-id:n. ... ok
test_plant_form_string_category (garden.tests.VirheellisetAssosiaatiotTest.test_plant_form_string_category)
PlantSpeciesForm hylkää merkkijonon kategoria-kentässä. ... ok
test_vaihda_tila_nonexistent_pk (garden.tests.VirheellisetAssosiaatiotTest.test_vaihda_tila_nonexistent_pk)
Olemattoman viljelymerkinnän PK tilan vaihdossa palauttaa 404. ... ok
test_viljely_detail_get_nonexistent_pk (garden.tests.VirheellisetAssosiaatiotTest.test_viljely_detail_get_nonexistent_pk)
Olemattoman viljelymerkinnän PK palauttaa 404. ... ok
test_viljely_detail_post_nonexistent_pk (garden.tests.VirheellisetAssosiaatiotTest.test_viljely_detail_post_nonexistent_pk)
Olemattoman viljelymerkinnän PK POST palauttaa 404. ... ok

----------------------------------------------------------------------
Ran 105 tests in 0.102s

OK
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
```
