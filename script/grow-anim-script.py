print "<<<-------Python Module FIRST STRING-------->>>"

def onImportPress():

    import _alembic_hom_extensions as abc
    import os
    global ga_node
    
    ga_node = hou.node('/obj/growanim/')
    print "---Import Button Begin---"
    #Variables
    global abc_path, cur_path
    abc_path = ga_node.parm('file_path').eval()
    #Paths from ABC file
    path_list = abc.alembicGetObjectPathListForMenu(abc_path)
    path_list = remove_duplicates(path_list)
    #Creating Subnet Node
    main_sub_node = hou.node("/obj/").createNode("subnet", node_name = os.path.basename(abc_path)[:-4]+"_GrowAnim")
    group_sub_item = 0
    #Creating GEO for each mesh
    for cur_path in path_list:
        if abc.alembicGetSceneHierarchy(abc_path, cur_path)[1] == "polymesh":
            cur_path_list = list(cur_path[1:].split("/"))
            exist_ = False
            for child in main_sub_node.children():
                if child.name() == cur_path_list[0]+"_Group":
                    exist_ = True
            if exist_ == False:
                group_sub_node = main_sub_node.createNode("subnet", node_name = cur_path_list[0]+"_Group")
                group_sub_item = 0
            anim_sub_node = group_sub_node.createNode("subnet", node_name = cur_path_list[-1]+"_Anim")
            anim_sub_node.setColor(hou.Color([0.65,0.9,0.15]))
            anim_sub_node.setPosition([0, group_sub_item * (-1)])
            abc_nodes_create(anim_sub_node, cur_path, cur_path_list, group_sub_item)
            group_sub_item += 1
    #Layout Children
    main_sub_node.layoutChildren()
    #Creating AnimGrow Parms
    for child_node in main_sub_node.children():
        parms_create(child_node)
    print "---Import Button End---"  
    
def abc_scale():
    units  =  [0.0254, 0.01, 1]
    u_from =  units[ga_node.parm("conv_from").eval()]
    u_to   =  units[ga_node.parm("conv_to").eval()]
    return u_from/u_to

def remove_duplicates(l):
    final_list = []
    for w in l:
        if w not in final_list:
            final_list.append(w)
    return final_list
       
def abc_nodes_create(root_node, cur_path, cur_path_list, group_sub_item):
    geo_node = root_node.createNode("geo", node_name = cur_path_list[-1])
    abc_node = geo_node.createNode("alembic")
    abc_node.parm("fileName").set(abc_path)
    abc_node.parm("objectPath").set(cur_path)
    abc_node.parm("loadmode").set(1)
    xform_node = geo_node.createNode("xform", node_name = "Scale")
    xform_node.parm("scale").set(abc_scale())
    xform_node.setFirstInput(abc_node)
    null_node = geo_node.createNode("null", node_name = "OUT_abc")
    null_node.setFirstInput(xform_node)
    null_node.setDisplayFlag(True)
    null_node.setRenderFlag(True)   
    geo_node.layoutChildren()
    if len(cur_path_list) == 2:
        root_node.layoutChildren()
    return 0
    
def parms_create(root_node):
#    ptg = root_node.parmTemplateGroup()
#    parm_folder = hou.FolderParmTemplate('anim_set', 'AnimSettings')
#    parm_folder.addParmTemplate(hou.IntParmTemplate('duration', 'Duration', 1, default_value = ([18])))
#    parm_folder.addParmTemplate(hou.IntParmTemplate('lag', 'Lag', 1, default_value = ([0])))
#    parm_folder.addParmTemplate(hou.IntParmTemplate('lag_inside', 'Lag Inside', 1, default_value = ([2])))
#    ptg.append(parm_folder)
#    root_node.setParmTemplateGroup(ptg)
#    root_node.parm('lag').setExpression("round(hou.node('.').position()[1]*(-1))*2", language = hou.exprLanguage.Python)
#    ptg = sel.parmTemplateGroup()
#    parm_folder = hou.FolderParmTemplate('anim_set', 'AnimSettings')
#    parm_folder.addParmTemplate(hou.IntParmTemplate('duration', 'Duration', 1, default_value = ([24])))
#    parm_folder.addParmTemplate(hou.IntParmTemplate('lag', 'Lag', 1, default_value = ([0])))
#    parm_folder.addParmTemplate(hou.IntParmTemplate('lag_inside', 'Lag Inside', 1, default_value = ([2])))
#    ptg.append(parm_folder)
#    sel.setParmTemplateGroup(ptg)


    # Code for parameter template
#    hou_parm_template = hou.FolderParmTemplate("stdswitcher4_5", "AnimSettings", folder_type=hou.folderType.
#    Tabs, default_value=0, ends_tab_group=False)

    ptg = root_node.parmTemplateGroup()
    hou_parm_template = hou.FolderParmTemplate('anim_set', 'AnimSettings')
    
    
    
    # anim_type
    hou_parm_template2 = hou.MenuParmTemplate("anim_type", "Anim Type", menu_items=(["scale","sc_corner","sc_uniform","rot",
                            "slice"]), menu_labels=(["Scale","Scale Corner","Scale Uniform","Rotation","Slice"]), default_value=0, 
                            icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python,
                            menu_type=hou.menuType.Normal, menu_use_token=False, is_button_strip=False, strip_uses_icons=False)
    hou_parm_template2.setJoinWithNext(True)
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # axis_scale
    hou_parm_template2 = hou.MenuParmTemplate("axis_scale", "  Axis", menu_items=(["x","y","z","-x","-y","-z"]), menu_labels=(["X",
                            "Y","Z","-X","-Y","-Z"]), default_value=1, icon_names=([]), item_generator_script="", 
                            item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False,
                            is_button_strip=False, strip_uses_icons=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != scale }")
    hou_parm_template2.setJoinWithNext(True)
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # axis_sc_corner
    hou_parm_template2 = hou.MenuParmTemplate("axis_sc_corner", "  Axis", menu_items=(["xz","-xz","-x-z","x-z"]), menu_labels=(["X,Z","-X,Z","-X,-Z","X,-Z"]),
                            default_value=3, icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python,
                            menu_type=hou.menuType.Normal, menu_use_token=False, is_button_strip=False, strip_uses_icons=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != sc_corner }")
    hou_parm_template2.setJoinWithNext(True)
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # axis_sc_uniform
    hou_parm_template2 = hou.MenuParmTemplate("axis_sc_uniform", "  Axis", menu_items=(["center","x","y","z","-x","-y","-z"]),
                            menu_labels=(["center","X","Y","Z","-X","-Y","-Z"]), default_value=2, icon_names=([]), item_generator_script="",
                            item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False,
                            is_button_strip=False, strip_uses_icons=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != sc_uniform }")
    hou_parm_template2.setJoinWithNext(True)
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # axis_rot
    hou_parm_template2 = hou.MenuParmTemplate("axis_rot", "  Axis", menu_items=(["x","z","-x","-z"]), menu_labels=(["X","Z","-X","-Z"]),
                            default_value=0, icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python,
                            menu_type=hou.menuType.Normal, menu_use_token=False, is_button_strip=False, strip_uses_icons=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != rot }")
    hou_parm_template2.setJoinWithNext(True)
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # axis_slice
    hou_parm_template2 = hou.MenuParmTemplate("axis_slice", "  Axis", menu_items=(["x","y","z","-x","-y","-z"]),
                            menu_labels=(["X","Y","Z","-X","-Y","-Z"]), default_value=1, icon_names=([]), item_generator_script="",
                            item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False,
                            is_button_strip=False, strip_uses_icons=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != slice }")
    hou_parm_template2.setJoinWithNext(True)    
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # update
    hou_parm_template2 = hou.ButtonParmTemplate("update", "Update Animation")
    hou_parm_template2.setScriptCallback("hou.node('/obj/growanim/').hdaModule().onGrowAnimPress(kwargs)")
    hou_parm_template2.setScriptCallbackLanguage(hou.scriptLanguage.Python)
    hou_parm_template2.setTags({"script_callback": "hou.node('/obj/growanim/').hdaModule().onGrowAnimPress(kwargs)",
                            "script_callback_language": "python"})
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # dur_scale
    hou_parm_template2 = hou.IntParmTemplate("dur_scale", "Duration", 1, default_value=([12]), min=0, max=30,min_is_strict=False,
                            max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]),
                            item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal,
                            menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != scale }")
    hou_parm_template2.setJoinWithNext(True)
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # overshoot_scale
    hou_parm_template2 = hou.FloatParmTemplate("overshoot_scale", "Overshoot", 1, default_value=([0.05]), min=0, max=0.5, min_is_strict=False,
                            max_is_strict=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != scale }")
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # lag_scale
    hou_parm_template2 = hou.IntParmTemplate("lag_scale", "Lag", 1, default_value=([1]), min=0, max=10, min_is_strict=False, max_is_strict=False,
                            naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="",
                            item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != scale }")
    hou_parm_template2.setJoinWithNext(True)
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # lag_mult_scale
    hou_parm_template2 = hou.IntParmTemplate("lag_mult_scale", "Lag Mult", 1, default_value=([1]), min=1, max=5, min_is_strict=False,
                            max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]),
                            item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal,
                            menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != scale }")
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # lag_inside_scale
    hou_parm_template2 = hou.IntParmTemplate("lag_inside_scale", "Lag Inside", 1, default_value=([2]), min=0, max=5, min_is_strict=False,
                            max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]),
                            item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal,
                            menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != scale }")
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # dur_sc_corner
    hou_parm_template2 = hou.IntParmTemplate("dur_sc_corner", "Duration", 1, default_value=([12]), min=0, max=30, min_is_strict=False,
                            max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]),
                            item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal,
                            menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != sc_corner }")
    hou_parm_template2.setJoinWithNext(True)
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # overshoot_sc_corner
    hou_parm_template2 = hou.FloatParmTemplate("overshoot_sc_corner", "Overshoot", 1, default_value=([0.05]), min=0, max=0.5, min_is_strict=False,
                            max_is_strict=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != sc_corner }")
    hou_parm_template.addParmTemplate(hou_parm_template2)    
    # lag_sc_corner
    hou_parm_template2 = hou.IntParmTemplate("lag_sc_corner", "Lag", 1, default_value=([0]), min=0, max=10, min_is_strict=False,
                            max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]),
                            item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal,
                            menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != sc_corner }")
    hou_parm_template2.setJoinWithNext(True)
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # lag_mult_sc_corner
    hou_parm_template2 = hou.IntParmTemplate("lag_mult_sc_corner", "Lag Mult", 1, default_value=([1]), min=0, max=5, min_is_strict=False,
                            max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]),
                            item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal,
                            menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != sc_corner }")
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # lag_inside_sc_corner
    hou_parm_template2 = hou.IntParmTemplate("lag_inside_sc_corner", "Lag Inside", 1, default_value=([2]), min=0, max=5, min_is_strict=False,
                            max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]),
                            item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal,
                            menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != sc_corner }")
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # dur_sc_uniform
    hou_parm_template2 = hou.IntParmTemplate("dur_sc_uniform", "Duration", 1, default_value=([12]), min=0, max=30, min_is_strict=False,
                            max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]),
                            item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal,
                            menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != sc_uniform }")
    hou_parm_template2.setJoinWithNext(True)
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # overshoot_sc_uniform
    hou_parm_template2 = hou.FloatParmTemplate("overshoot_sc_uniform", "Overshoot", 1, default_value=([0.05]), min=0, max=0.5, min_is_strict=False,
                            max_is_strict=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != sc_uniform }")
    hou_parm_template.addParmTemplate(hou_parm_template2)    
    # lag_sc_uniform
    hou_parm_template2 = hou.IntParmTemplate("lag_sc_uniform", "Lag", 1, default_value=([0]), min=0, max=10, min_is_strict=False,
                            max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]),
                            item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal,
                            menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != sc_uniform }")
    hou_parm_template2.setJoinWithNext(True)
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # lag_mult_sc_uniform
    hou_parm_template2 = hou.IntParmTemplate("lag_mult_sc_uniform", "Lag Mult", 1, default_value=([1]), min=0, max=5, min_is_strict=False,
                            max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]),
                            item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal,
                            menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != sc_uniform }")
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # lag_inside_sc_uniform
    hou_parm_template2 = hou.IntParmTemplate("lag_inside_sc_uniform", "Lag Inside", 1, default_value=([2]), min=0, max=5, min_is_strict=False,
                            max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]),
                            item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal,
                            menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != sc_uniform }")
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # dur_rot
    hou_parm_template2 = hou.IntParmTemplate("dur_rot", "Duration", 1, default_value=([12]), min=0, max=30, min_is_strict=False, max_is_strict=False,
                            naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="",
                            item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != rot }")
    hou_parm_template2.setJoinWithNext(True)
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # overshoot_rot
    hou_parm_template2 = hou.FloatParmTemplate("overshoot_rot", "Overshoot", 1, default_value=([0.05]), min=0, max=0.5, min_is_strict=False,
                            max_is_strict=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != rot }")
    hou_parm_template.addParmTemplate(hou_parm_template2)    
    # lag_rot
    hou_parm_template2 = hou.IntParmTemplate("lag_rot", "Lag", 1, default_value=([0]), min=0, max=10, min_is_strict=False, max_is_strict=False,
                            naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="",
                            item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != rot }")
    hou_parm_template2.setJoinWithNext(True)
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # lag_mult_rot
    hou_parm_template2 = hou.IntParmTemplate("lag_mult_rot", "Lag Mult", 1, default_value=([1]), min=0, max=5, min_is_strict=False,
                            max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]),
                            item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal,
                            menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != rot }")
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # lag_inside_rot
    hou_parm_template2 = hou.IntParmTemplate("lag_inside_rot", "Lag Inside", 1, default_value=([2]), min=0, max=5, min_is_strict=False, 
                            max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]),
                            item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal,
                            menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != rot }")
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # dur_slice
    hou_parm_template2 = hou.IntParmTemplate("dur_slice", "Duration", 1, default_value=([12]), min=0, max=30, min_is_strict=False, max_is_strict=False,
                            naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="",
                            item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != slice }")
    hou_parm_template2.setJoinWithNext(True)    
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # overshoot_slice
    hou_parm_template2 = hou.FloatParmTemplate("overshoot_slice", "Overshoot", 1, default_value=([0.05]), min=0, max=0.5, min_is_strict=False,
                            max_is_strict=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != slice }")
    hou_parm_template.addParmTemplate(hou_parm_template2)    
    # lag_slice
    hou_parm_template2 = hou.IntParmTemplate("lag_slice", "Lag", 1, default_value=([0]), min=0, max=10, min_is_strict=False, max_is_strict=False,
                            naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="",
                            item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != slice }")
    hou_parm_template2.setJoinWithNext(True)
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # lag_mult_slice
    hou_parm_template2 = hou.IntParmTemplate("lag_mult_slice", "Lag Mult", 1, default_value=([1]), min=0, max=5, min_is_strict=False,
                            max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]),
                            item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal,
                            menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != slice }")
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # lag_inside_slice
    hou_parm_template2 = hou.IntParmTemplate("lag_inside_slice", "Lag Inside", 1, default_value=([2]), min=0, max=5, min_is_strict=False,
                            max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]),
                            item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal,
                            menu_use_token=False)
    hou_parm_template2.setConditional(hou.parmCondType.HideWhen, "{ anim_type != slice }")
    hou_parm_template.addParmTemplate(hou_parm_template2) 
          
    ptg.append(hou_parm_template)
    root_node.setParmTemplateGroup(ptg)
    root_node.parm('lag_scale').setExpression("round(hou.node('.').position()[1]*(-1))*2", language = hou.exprLanguage.Python)
    root_node.parm('lag_sc_corner').setExpression("round(hou.node('.').position()[1]*(-1))*2", language = hou.exprLanguage.Python)
    root_node.parm('lag_sc_uniform').setExpression("round(hou.node('.').position()[1]*(-1))*2", language = hou.exprLanguage.Python)
    root_node.parm('lag_rot').setExpression("round(hou.node('.').position()[1]*(-1))*2", language = hou.exprLanguage.Python)
    root_node.parm('lag_slice').setExpression("round(hou.node('.').position()[1]*(-1))*2", language = hou.exprLanguage.Python)
    


def onGrowAnimPress(kwargs_import):
    print "--- onGrowAnimPress START -----"
    #Globals
    global anim_type, axis, dur, lag, lag_mult, lag_inside, overshoot
    global max_y_pos
    #Main Sub Node
    main_sub_node = kwargs_import['node'].parent()
    #Remove Nulls
    for group_sub_node in main_sub_node.children():
        for anim_sub_node in group_sub_node.children():
            for n in anim_sub_node.children():
                if n.type().name() == "null":
                    n.destroy()
    #Loop
    for group_sub_node in main_sub_node.children():
        #Read Anim Parameters
        anim_type = group_sub_node.parm('anim_type').evalAsString()
        print group_sub_node, anim_type
        #Calculation max_y_pos
        max_y_pos = int(round(group_sub_node.children()[0].position()[1]))
        for anim_sub_node in group_sub_node.children():
            if int(round(anim_sub_node.position()[1])) > max_y_pos:
                max_y_pos = int(round(anim_sub_node.position()[1]))
        #If "scale"
        if anim_type == "scale":
            axis        =  group_sub_node.parm('axis_scale').evalAsString()
            dur         =  group_sub_node.parm('dur_scale').eval()
            lag         =  group_sub_node.parm('lag_scale').eval()
            lag_mult    =  group_sub_node.parm('lag_mult_scale').eval()
            lag_inside  =  group_sub_node.parm('lag_inside_scale').eval()
            overshoot   =  group_sub_node.parm('overshoot_scale').eval()
            #Anim Nodes Creation
            for anim_sub_node in group_sub_node.children():
                anim_nodes_for_scale(anim_sub_node)
                
        #If "sc_corner"
        if anim_type == "sc_corner":
            axis        =  group_sub_node.parm('axis_sc_corner').evalAsString()
            dur         =  group_sub_node.parm('dur_sc_corner').eval()
            lag         =  group_sub_node.parm('lag_sc_corner').eval()
            lag_mult    =  group_sub_node.parm('lag_mult_sc_corner').eval()
            lag_inside  =  group_sub_node.parm('lag_inside_sc_corner').eval()
            overshoot   =  group_sub_node.parm('overshoot_sc_corner').eval()
            #Anim Nodes Creation
            for anim_sub_node in group_sub_node.children():
                anim_nodes_for_sc_corner(anim_sub_node)

        #If "sc_uniform"
        if anim_type == "sc_uniform":
            axis        =  group_sub_node.parm('axis_sc_uniform').evalAsString()
            dur         =  group_sub_node.parm('dur_sc_uniform').eval()
            lag         =  group_sub_node.parm('lag_sc_uniform').eval()
            lag_mult    =  group_sub_node.parm('lag_mult_sc_uniform').eval()
            lag_inside  =  group_sub_node.parm('lag_inside_sc_uniform').eval()
            overshoot   =  group_sub_node.parm('overshoot_sc_uniform').eval()
            #Anim Nodes Creation
            for anim_sub_node in group_sub_node.children():
                anim_nodes_for_sc_uniform(anim_sub_node)                 
                
                
        
            
    print "--- onGrowAnimPress END -----"


def anim_nodes_for_scale(anim_sub_node):
    print "---- anim_nodes_for_scale BEGIN ----"
    # Bounding Box to b_box
    geo_node = anim_sub_node.children()[0]
    geo = hou.node(geo_node.path()+"/OUT_abc").geometry()
    b_box = geo.boundingBox()
    bb_min = b_box.minvec()
    bb_max = b_box.maxvec()
    bb_center = b_box.center()
    # Start Frame
    start_frame = lag*lag_mult + lag_inside*(round(anim_sub_node.position()[1])-max_y_pos)*(-1)
    # Null Node Creation
    null_node = geo_node.createInputNode(0,"null", node_name = "anim")
    null_node.setDisplayFlag(False)
    
    # Null Node Parameters and Keys
    if axis == "x":
        null_node.parm('px').set(bb_min[0])
        null_node.parm('py').set(bb_center[1])
        null_node.parm('pz').set(bb_center[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),2+start_frame,1) 
        set_key(null_node.parm("sz"),2+start_frame,1)      
        set_key(null_node.parm("sx"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sx"),int(round(dur + dur/3 + 1 + start_frame)),1)
    if axis == "y":
        null_node.parm('px').set(bb_center[0])
        null_node.parm('py').set(bb_min[1])
        null_node.parm('pz').set(bb_center[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sx"),2+start_frame,1) 
        set_key(null_node.parm("sz"),2+start_frame,1)      
        set_key(null_node.parm("sy"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sy"),int(round(dur + dur/3 + 1 + start_frame)),1)
    if axis == "z":
        null_node.parm('px').set(bb_center[0])
        null_node.parm('py').set(bb_center[1])
        null_node.parm('pz').set(bb_min[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sx"),2+start_frame,1) 
        set_key(null_node.parm("sy"),2+start_frame,1)      
        set_key(null_node.parm("sz"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sz"),int(round(dur + dur/3 + 1 + start_frame)),1)
    if axis == "-x":
        null_node.parm('px').set(bb_max[0])
        null_node.parm('py').set(bb_center[1])
        null_node.parm('pz').set(bb_center[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),2+start_frame,1) 
        set_key(null_node.parm("sz"),2+start_frame,1)      
        set_key(null_node.parm("sx"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sx"),int(round(dur + dur/3 + 1 + start_frame)),1)
    if axis == "-y":
        null_node.parm('px').set(bb_center[0])
        null_node.parm('py').set(bb_max[1])
        null_node.parm('pz').set(bb_center[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sx"),2+start_frame,1) 
        set_key(null_node.parm("sz"),2+start_frame,1)      
        set_key(null_node.parm("sy"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sy"),int(round(dur + dur/3 + 1 + start_frame)),1)
    if axis == "-z":
        null_node.parm('px').set(bb_center[0])
        null_node.parm('py').set(bb_center[1])
        null_node.parm('pz').set(bb_max[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sx"),2+start_frame,1) 
        set_key(null_node.parm("sy"),2+start_frame,1)      
        set_key(null_node.parm("sz"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sz"),int(round(dur + dur/3 + 1 + start_frame)),1)
    
    print "---- anim_nodes_for_scale END ----"

def anim_nodes_for_sc_corner(anim_sub_node):
    print "---- anim_nodes_for_sc_corner BEGIN ----"
    # Bounding Box to b_box
    geo_node = anim_sub_node.children()[0]
    geo = hou.node(geo_node.path()+"/OUT_abc").geometry()
    b_box = geo.boundingBox()
    bb_min = b_box.minvec()
    bb_max = b_box.maxvec()
    bb_center = b_box.center()
    # Start Frame
    start_frame = lag*lag_mult + lag_inside*(round(anim_sub_node.position()[1])-max_y_pos)*(-1)
    # Null Node Creation
    null_node = geo_node.createInputNode(0,"null", node_name = "anim")
    null_node.setDisplayFlag(False)   
    # Null Node Parameters and Keys
    if axis == "xz":
        null_node.parm('px').set(bb_max[0])
        null_node.parm('py').set(bb_center[1])
        null_node.parm('pz').set(bb_max[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),2+start_frame,1) 
        set_key(null_node.parm("sx"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sz"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sx"),int(round(dur + dur/3 + 1 + start_frame)),1)        
        set_key(null_node.parm("sz"),int(round(dur + dur/3 + 1 + start_frame)),1)
    if axis == "-xz":
        null_node.parm('px').set(bb_min[0])
        null_node.parm('py').set(bb_center[1])
        null_node.parm('pz').set(bb_max[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),2+start_frame,1) 
        set_key(null_node.parm("sx"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sz"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sx"),int(round(dur + dur/3 + 1 + start_frame)),1)        
        set_key(null_node.parm("sz"),int(round(dur + dur/3 + 1 + start_frame)),1)
    if axis == "-x-z":
        null_node.parm('px').set(bb_min[0])
        null_node.parm('py').set(bb_center[1])
        null_node.parm('pz').set(bb_min[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),2+start_frame,1) 
        set_key(null_node.parm("sx"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sz"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sx"),int(round(dur + dur/3 + 1 + start_frame)),1)        
        set_key(null_node.parm("sz"),int(round(dur + dur/3 + 1 + start_frame)),1)
    if axis == "x-z":
        null_node.parm('px').set(bb_max[0])
        null_node.parm('py').set(bb_center[1])
        null_node.parm('pz').set(bb_min[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),2+start_frame,1) 
        set_key(null_node.parm("sx"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sz"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sx"),int(round(dur + dur/3 + 1 + start_frame)),1)        
        set_key(null_node.parm("sz"),int(round(dur + dur/3 + 1 + start_frame)),1)
    print "---- anim_nodes_for_sc_corner END ----"    

    
def anim_nodes_for_sc_uniform(anim_sub_node):
    print "---- anim_nodes_for_sc_uniform BEGIN ----"
    # Bounding Box to b_box
    geo_node = anim_sub_node.children()[0]
    geo = hou.node(geo_node.path()+"/OUT_abc").geometry()
    b_box = geo.boundingBox()
    bb_min = b_box.minvec()
    bb_max = b_box.maxvec()
    bb_center = b_box.center()
    # Start Frame
    start_frame = lag*lag_mult + lag_inside*(round(anim_sub_node.position()[1])-max_y_pos)*(-1)
    # Null Node Creation
    null_node = geo_node.createInputNode(0,"null", node_name = "anim")
    null_node.setDisplayFlag(False)
    
    # Null Node Parameters and Keys
    if axis == "center":
        null_node.parm('px').set(bb_center[0])
        null_node.parm('py').set(bb_center[1])
        null_node.parm('pz').set(bb_center[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sx"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sy"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sz"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sx"),int(round(dur + dur/3 + 1 + start_frame)),1)
        set_key(null_node.parm("sy"),int(round(dur + dur/3 + 1 + start_frame)),1)
        set_key(null_node.parm("sz"),int(round(dur + dur/3 + 1 + start_frame)),1)        
    if axis == "x":
        null_node.parm('px').set(bb_min[0])
        null_node.parm('py').set(bb_center[1])
        null_node.parm('pz').set(bb_center[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sx"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sy"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sz"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sx"),int(round(dur + dur/3 + 1 + start_frame)),1)
        set_key(null_node.parm("sy"),int(round(dur + dur/3 + 1 + start_frame)),1)
        set_key(null_node.parm("sz"),int(round(dur + dur/3 + 1 + start_frame)),1) 
    if axis == "y":
        null_node.parm('px').set(bb_center[0])
        null_node.parm('py').set(bb_min[1])
        null_node.parm('pz').set(bb_center[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sx"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sy"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sz"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sx"),int(round(dur + dur/3 + 1 + start_frame)),1)
        set_key(null_node.parm("sy"),int(round(dur + dur/3 + 1 + start_frame)),1)
        set_key(null_node.parm("sz"),int(round(dur + dur/3 + 1 + start_frame)),1) 
    if axis == "z":
        null_node.parm('px').set(bb_center[0])
        null_node.parm('py').set(bb_center[1])
        null_node.parm('pz').set(bb_min[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sx"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sy"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sz"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sx"),int(round(dur + dur/3 + 1 + start_frame)),1)
        set_key(null_node.parm("sy"),int(round(dur + dur/3 + 1 + start_frame)),1)
        set_key(null_node.parm("sz"),int(round(dur + dur/3 + 1 + start_frame)),1) 
    if axis == "-x":
        null_node.parm('px').set(bb_max[0])
        null_node.parm('py').set(bb_center[1])
        null_node.parm('pz').set(bb_center[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sx"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sy"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sz"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sx"),int(round(dur + dur/3 + 1 + start_frame)),1)
        set_key(null_node.parm("sy"),int(round(dur + dur/3 + 1 + start_frame)),1)
        set_key(null_node.parm("sz"),int(round(dur + dur/3 + 1 + start_frame)),1) 
    if axis == "-y":
        null_node.parm('px').set(bb_center[0])
        null_node.parm('py').set(bb_max[1])
        null_node.parm('pz').set(bb_center[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sx"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sy"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sz"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sx"),int(round(dur + dur/3 + 1 + start_frame)),1)
        set_key(null_node.parm("sy"),int(round(dur + dur/3 + 1 + start_frame)),1)
        set_key(null_node.parm("sz"),int(round(dur + dur/3 + 1 + start_frame)),1) 
    if axis == "-z":
        null_node.parm('px').set(bb_center[0])
        null_node.parm('py').set(bb_center[1])
        null_node.parm('pz').set(bb_max[2])
        set_key(null_node.parm("sx"),1+start_frame,0.001)
        set_key(null_node.parm("sy"),1+start_frame,0.001)
        set_key(null_node.parm("sz"),1+start_frame,0.001)
        set_key(null_node.parm("sx"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sy"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sz"),dur+1+start_frame,1+overshoot)
        set_key(null_node.parm("sx"),int(round(dur + dur/3 + 1 + start_frame)),1)
        set_key(null_node.parm("sy"),int(round(dur + dur/3 + 1 + start_frame)),1)
        set_key(null_node.parm("sz"),int(round(dur + dur/3 + 1 + start_frame)),1) 
    
    print "---- anim_nodes_for_sc_uniform END ----"
    
    
    
    
    
def set_key(parm,frame,value):
    key = hou.Keyframe()
    key.setValue(value)
    key.setFrame(frame)
    key.setSlopeAuto(True)
    key.setInSlopeAuto(True)
    
    parm.setKeyframe(key)
    return 0


print "---------Python Module LAST STRING----------"

