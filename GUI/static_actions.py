from PyQt5.QtWidgets import QAction
from .GUI_Resources import *

class StaticActions:
    print("something")
    add = get_add_icon()
    edit = get_edit_icon()
    delete = get_delete_icon()
    save = get_save_icon()
    reload = get_reload_icon()
    visible = get_shown_icon()
    hidden = get_hidden_icon()
    json = get_json_icon()
    xml = get_xml_icon()
    db = get_db_icon()
    user = get_user_icon()
    filesystem = get_filesystem_icon()
    camera = get_camera_icon()
    add_pacient_action = QAction(add, "&Añadir paciente")
    edit_pacient_action = QAction(edit,"&Editar paciente")
    del_pacient_action = QAction(delete,"&Eliminar paciente")
    #add_pacient_action = QAction( "&Añadir")
    #edit_pacient_action = QAction("&Editar")
    #del_pacient_action = QAction("&Eliminar")
    recargar_action = QAction(reload,"Recargar datos")
    consultar_tablas_action = QAction("Consultar tablas SQL")
    exportar_JSON_action = QAction(json,"Exportar JSON")
    exportar_XML_action = QAction(xml,"Exportar XML")
    add_prueba_action = QAction(add,"Añadir prueba")
    edit_prueba_action = QAction(edit, "Modificar prueba")
    del_prueba_action = QAction(delete,"Eliminar prueba")
    creditos_action = QAction("Creditos")
    vista_toolbar = QAction(visible,"Barra de herramientas.")
    vista_crono = QAction(visible,"Vista cronometro.")
    vista_pacientes = QAction(visible,"Vista pacientes.")
    vista_rendimiento = QAction(visible,"Vista rendimiento.")

    tomar_foto = QAction(camera,"Tomar foto")
    seleccionar_foto = QAction(filesystem,"Buscar nueva foto.")


    vista_toolbar.setObjectName("action_view_toolbar")
    vista_crono.setObjectName("action_view_crono")
    vista_pacientes.setObjectName("action_view_pacientes")
    vista_rendimiento.setObjectName("action_view_rendimiento")
    add_pacient_action.setObjectName("add_pacient_action")
    edit_pacient_action.setObjectName("edit_pacient_action")
    del_pacient_action.setObjectName("del_pacient_action")
    recargar_action.setObjectName("reload_db_action")
    consultar_tablas_action.setObjectName("see_db_structure_action")
    exportar_JSON_action.setObjectName("export_json_action")
    exportar_XML_action.setObjectName("export_xml_action")
    edit_prueba_action.setObjectName("mod_prueba_action")
    del_prueba_action.setObjectName("del_prueba_action")
    creditos_action.setObjectName("creditos_action")
    tomar_foto.setObjectName("tomar_foto")
    seleccionar_foto.setObjectName("seleccionar_foto")