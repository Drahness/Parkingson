from PyQt5.QtWidgets import QAction
from .GUI_Resources import *

class StaticActions:
    print("something")
    add = get_add_icon()
    edit = get_edit_icon()
    delete = get_delete_icon()
    save = get_save_icon()
    add_pacient_action = QAction(add, "&Añadir")
    edit_pacient_action = QAction(edit,"&Editar")
    del_pacient_action = QAction(delete,"&Eliminar")
    #add_pacient_action = QAction( "&Añadir")
    #edit_pacient_action = QAction("&Editar")
    #del_pacient_action = QAction("&Eliminar")
    recargar_action = QAction("Recargar datos")
    consultar_tablas_action = QAction("Consultar tablas SQL")
    exportar_JSON_action = QAction("Exportar JSON")
    exportar_XML_action = QAction("Exportar XML")
    mod_prueba_action = QAction("Modificar prueba")
    del_prueba_action = QAction("Eliminar prueba")
    creditos_action = QAction("Creditos")



    add_pacient_action.setObjectName("add_pacient_action")
    edit_pacient_action.setObjectName("edit_pacient_action")
    del_pacient_action.setObjectName("del_pacient_action")
    recargar_action.setObjectName("reload_db_action")
    consultar_tablas_action.setObjectName("see_db_structure_action")
    exportar_JSON_action.setObjectName("export_json_action")
    exportar_XML_action.setObjectName("export_xml_action")
    mod_prueba_action.setObjectName("mod_prueba_action")
    del_prueba_action.setObjectName("del_prueba_action")
    creditos_action.setObjectName("creditos_action")