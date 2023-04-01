import sys
orgsts = sys.stdout
#sys.stdout = open("logs\\session.log", "w")
from ursina import *
from ursina.shaders import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.prefabs.file_browser import *
import subprocess, command
from threading import Thread
import PyInstaller.__main__
import time
from zipfile import ZipFile as zf






app = Ursina(vsync = True, borderless = False, fullscreen = False, debug = False)
window.title = "Ursina game engine"
window.icon = "IMG\\logo.ico"

camera.aspect_ratio = 0.778

name = "Temp"

scene.fog_density = .1
scene.fog_density = (50, 200)
Entity.deafault_shader  = lit_with_shadows_shader

#Functions
def addToScene(model):
    global entities, amount
    e = None
    if model == "light":
        try:
            amount["Light"] += 1
        except:
            amount["Light"] = 1
        e = DirectionalLight(x = 30, y = 40, strmodel = "AmbientLight", typeof = "light", shadows = True, lookat = (1,-1,1), hasBehaviour = False)
        e.look_at(e.lookat)
        entitiesr.append(e)
    elif model == "player":
        e = Entity(model = "cube", color = color.white, strmodel = "cube", typeof = "player", hasBehaviour = False, shader  = lit_with_shadows_shader)
        entitiesr.append(e)
    elif model == "import":
        try:    
            amount[model] += 1
        except:
            amount[model] = 1
        fb = FileBrowser(file_types=(['.zip']), enabled=True, hasBehaviour = False)
        g = []
        
        def on_submit(paths):
            e = None
            for p in paths:
                g.append(p)
            for i in g:
                
                f = str(i).split("\\")
                f = f[len(f)-1]
                p = str(i).split("\\")
                pat = []
                for pt in p:
                    if p.index(pt) != len(p)-1:
                        pat.append(pt) 
                p = "\\".join(pat)
                os.system(f'cd {p} & COPY {f} "{os.getcwd()}/models"')
                with zf(f"{os.getcwd()}/models/{f}", "r") as zif:
                    zif.extractall(f"{os.getcwd()}/models")
                    os.system(f'DEL "{os.getcwd()}/models/{f}"')
                    f = "".join(f).split(".")[0]+".obj"
                e = Entity(model = f, strmodel = str(model)+str(amount[model]), color = color.random_color(), collider = "Mesh", typeof = "mesh", hasBehaviour = False, shader  = lit_with_shadows_shader)
                entitiesr.append(e)
        fb.on_submit = on_submit
    else:
        
        try:    
            amount[model] += 1
        except:
            amount[model] = 1
        e = Entity(model = model, strmodel = str(model)+str(amount[model]), color = color.random_color(), collider = "Mesh", typeof = "mesh", hasBehaviour = False)
        entitiesr.append(e)

def gizmo(entitie):
    if entitie.type != None:
        def abeh():
            entitie.hasBehaviour = True
            behBTN.disable()
            ebehBTN.enable()
        def ebeh():
            exec(open("editor_main.py").read())
        def scale():
            entitie.scale_x = xscaler.value
            entitie.scale_y = yscaler.value
            entitie.scale_z = zscaler.value
        def repos():
            entitie.x = xsl.value
            entitie.y = ysl.value
            entitie.z = zsl.value
        def rerot():
            entitie.rotation_x = xr.value
            entitie.rotation_y = yr.value
            entitie.rotation_z = zr.value
        def recol():
            entitie.color = (r.value,g.value,b.value,a.value)
        def c():
            try:
                wp.disable()
            except:
                pass
            wp2.disable()
        xscaler = ThinSlider(min= 0, max = 10, on_value_changed = scale, value = 1.0, dynamic = True)
        yscaler = ThinSlider(min= 0, max = 10, on_value_changed = scale, value = 1.0, dynamic = True)
        zscaler = ThinSlider(min= 0, max = 10, on_value_changed = scale, value = 1.0, dynamic = True)
        
        xsl = ThinSlider(min= -10, max = 10, on_value_changed = repos, value = 0.0, dynamic = True)
        ysl = ThinSlider(min= -10, max = 10, on_value_changed = repos, value = 0.0, dynamic = True)
        zsl = ThinSlider(min= -10, max = 10, on_value_changed = repos, value = 0.0, dynamic = True)
    
        xr = ThinSlider(min= -360, max = 360, on_value_changed = rerot, value = 0.0, dynamic = True)
        yr = ThinSlider(min= -360, max = 360, on_value_changed = rerot, value = 0.0, dynamic = True)
        zr = ThinSlider(min= -360, max = 360, on_value_changed = rerot, value = 0.0, dynamic = True)
    
        r = ThinSlider(min= -1, max = 1, on_value_changed = recol, value = entitie.color.x, dynamic = True)
        g = ThinSlider(min= -1, max = 1, on_value_changed = recol, value = entitie.color.y, dynamic = True)
        b = ThinSlider(min= -1, max = 1, on_value_changed = recol, value = entitie.color.z, dynamic = True)
        a = ThinSlider(min= 0, max = 1, on_value_changed = recol, value = entitie.color.w, dynamic = True)
    
        gizmoSliders = [xsl,ysl,zsl,xr,yr,zr,xscaler,yscaler,zscaler]
        
        cbtn = Button("close", on_click = c)
        if entitie.typeof == "mesh" or entitie.typeof == "player":
            wp = WindowPanel(title = entitie.strmodel, content = [
                Text("Scale"),
                xscaler,
                yscaler,
                zscaler,
                Text("Position(XYZ)"),
                xsl,ysl,zsl,
                Text("Rotation(XYZ)"),
                xr,yr,zr,
                Space(2),
                cbtn]
                     )
            behBTN = Button(text = "Add behaviour", on_click = abeh)
            ebehBTN = Button(text = "Edit behaviour", on_click = ebeh, enabled = False)
            wp2 = WindowPanel(title = entitie.typeof+"'s Color", content = [
                Space(1),
                behBTN,
                ebehBTN,
                Text("Color(RGBA)"),
                r,g,b,a
                ])
            if entitie.hasBehaviour:
                behBTN.disable()
                ebehBTN.enable()
            else:
                ebehBTN.disable()
        else:
            for i in gizmoSliders:
                i.disable()
            wp2 = WindowPanel(title = entitie.strmodel+"'s Color", content = [
                Text("Color(RGBA)"),
                r,g,b,a,
                Space(2),
                cbtn
                ])
        

#Variables
r_bdict = {}
l_bdict = {
    "AmbientLight" : Func(addToScene, "light"),
    "Cube": Func(addToScene, "cube"),
    "Sphere" : Func(addToScene, "sphere"),
    "Plane" : Func(addToScene, "plane"),
    "Import model": Func(addToScene, "import")
    }

amount = {}

#Saving and loading

def save():
    global name
    if not os.path.exists(f"projects\\{svn.text}"):
        if not os.path.exists("projects"):
            os.mkdir("projects")
        if not os.path.exists(f"projects\\{svn.text}"):
            os.mkdir(f"projects\\{svn.text}")
    with open(f"projects\\{svn.text}\\main.UGERsf", "w") as f:
        f.write(svn.text)
        for i in entitiesr:
            if i.strmodel == "AmbientLight":
                f.write(f"\n{str(i.model)};{str(i.position)};{str(i.color)};{str(i.rotation)};{str(i.scale)};{str(i.typeof)};{str(i.strmodel)};{str(i.lookat)}\n")
            else:
                f.write(f"\n{str(i.model)};{str(i.position)};{str(i.color)};{str(i.rotation)};{str(i.scale)};{str(i.typeof)};{str(i.strmodel)}\n")
    sv.disable()
    name = svn.text
    
svn = InputField()
sbtn = Button("Save", on_click = save)
sv = WindowPanel(name = "Save project", content = [svn, sbtn], enabled = False, popup = True)
    
def load(paths):
    e = None
    entitiesr.clear()
    g=[]
    for p in paths:
        g.append(p)
    for i in g:
        with open(i) as f:
            lines = f.read().split("\n")
            for e in lines:
                try:
                    el = e.split(";")
                    fcol = el[2].split("(")[1].split(")")[0]
                    rcol = fcol.split(",")
                    col = (float(rcol[0]), float(rcol[1]), float(rcol[2]), float(rcol[3]))

                    fsc = el[4].split("(")[1].split(")")[0]
                    rsc = fsc.split(",")
                    sc = (float(rsc[0]), float(rsc[1]), float(rsc[2]))

                    fpos = el[1].split("(")[1].split(")")[0]
                    rpos = fpos.split(",")
                    pos = (float(rpos[0]), float(rpos[1]), float(rpos[2]))

                    frot = el[3].split("(")[1].split(")")[0]
                    rrot = frot.split(",")
                    rot = (float(rrot[0]), float(rrot[1]), float(rrot[2]))

                    print(el[6])
                    Entity.deafault_shader  = lit_with_shadows_shader
                    if el[6] == "AmbientLight":
                        e = AmbientLight(x = pos[0], y = pos[1], shadows = True, strmodel = el[6], typeof = el[5], shader = colored_lights_shader)
                        frt = el[7].split("(")[1].split(")")[0]
                        rrt = frt.split(",")
                        rt = (float(rrt[0]), float(rrt[1]), float(rrt[2]))
                        e.look_at(rt)
                        entitiesr.append(e)
                    else:
                        e = Entity(model = el[0].split("/")[3], color = col, position = pos, rotation = rot, strmodel = el[6], typeof = el[5], scale = sc)
                        entitiesr.append(e)
                except Exception as e:
                    print("an error ocurred while excecuting load(), ignoring", type(e), "  \nerror:\n"+str(e))
    lm.disable()
    
lm = FileBrowser(file_types = [".UGERsf"], enabled = False, on_submit = load)


#UI
r_panel = Panel(scale_x = .5, x = .7)
r_txt = Text("In scene entities", x = .55, y = .45)
r_blist = ButtonList(r_bdict, parent = r_panel, scale_x = 1, y = .4)
l_panel = Panel(scale_x = .5, x = -.7)
l_txt = Text("Entitie prefabs", x = -.8, y = .45)
l_blist = ButtonList(l_bdict, parent = l_panel, scale_x = 1, y = .4)

#Scene



#Buildinfo:
entitiesr = []


#Building
def buildspec():
    if not os.path.exists(n.text):
        os.mkdir(n.text)
        os.mkdir(f"{n.text}\\{n.text}_data")
    with open("buildfiles\\main.py", "w") as f:
        f.write("from ursina import * \nfrom ursina.shaders import * \napp=Ursina()\nEntity.deafault_shader  = lit_with_shadows_shader\nEditorCamera()\n")
        for i in entitiesr:
            g = list(i.strmodel)
            g.pop(len(g)-1)
            m = str("".join(g))
            print(m)
            if m == "AmbientLigh":
                f.write(f"e=DirectionalLight(x = {i.x}, y = {i.y}, z = {i.z}, shadows = {i.shadows})\ne.look_at({i.lookat})\n")
            if m == "import":
                os.system(f'COPY {str(i.model).split("/")[3]} "{n.text}\\{n.text}_data"')
                f.write(f'Entity(model="{n.text}_data/{str(i.model).split("/")[3]}",color={str(i.color)},scale={str(i.scale)},position={str(i.position)}, rotation = {i.rotation})\n')
            else:
                f.write(f'Entity(model="{str(m)}",color={str(i.color)},scale={str(i.scale)},position={str(i.position)}, rotation = {i.rotation})\n')
        f.write("app.run()")
        f.close()

    
    libs = []
    time.sleep(1)
    for i in os.listdir("buildfiles\\alwaysinclude\\Lib\\site-packages"):
        libs.append(f'--add-data=buildfiles\\alwaysinclude\\Lib\\site-packages\\{i};{i}')
    cmd = f'color a & pyinstaller --windowed --onefile --name="{n.text}" {" ".join(libs)} "buildfiles\\main.py" & del {n.text}.spec & COPY dist\\{n.text}.exe \\{n.text} & xcopy models {n.text}\\{n.text}_data'
    print("\n\nGenerated build commans:\n"+cmd)
            
        
    os.system(cmd)
    os.system("copy dist\\{n.text}.exe {n.text}")
    print("Build complete")
    bs.disable()
def build():
    if not os.path.exists(n.text):
        os.mkdir(n.text)
        os.mkdir(f"{n.text}\\{n.text}_data")
    with open("buildfiles\\main.py", "w") as f:
        f.write("from ursina import * \nfrom ursina.shaders import * \napp=Ursina()\nEntity.deafault_shader  = lit_with_shadows_shader\n")
        for i in entitiesr:
            g = list(i.strmodel)
            g.pop(len(g)-1)
            m = str("".join(g))
            print(m)
            if m == "AmbientLigh":
                f.write(f"e=DirectionalLight(x = {i.x}, y = {i.y}, z = {i.z}, shadows = {i.shadows})\ne.look_at({i.lookat})\n")
            if m == "import":
                #os.system(f"copy {str(i.model).split('/')[3]} {n.text}\\{n.text}_data")
                os.system(f'COPY {str(i.model).split("/")[3]} "{n.text}\\{n.text}_data"')
                f.write(f'Entity(model="{n.text}_data/{str(i.model).split("/")[3]}",color={str(i.color)},scale={str(i.scale)},position={str(i.position)}, rotation = {i.rotation})\n')
                
            else:
                f.write(f'Entity(model="{str(m)}",color={str(i.color)},scale={str(i.scale)},position={str(i.position)}, rotation = {i.rotation})\n')
        f.write("app.run()")
        f.close()

    
    libs = []
    time.sleep(1)
    for i in os.listdir("buildfiles\\alwaysinclude\\Lib\\site-packages"):
        libs.append(f'--add-data=buildfiles\\alwaysinclude\\Lib\\site-packages\\{i};{i}')
    cmd = f'color a & pyinstaller --windowed --onefile --name="{n.text}" {" ".join(libs)} "buildfiles\\main.py" & del {n.text}.spec & COPY dist\\{n.text}.exe \\{n.text} & xcopy models {n.text}\\{n.text}_data'
    print("\n\nGenerated build commans:\n"+cmd)
    
            
        
    os.system(cmd)
    print("Build complete")
    bs.disable()
    
        


n = InputField()
bbtn = Button("Build Windowed", on_click = build)
bbbtn = Button("Build Console based", on_click = buildspec)
bs = WindowPanel("Build settings", enabled = False, content = [
    Space(),
    Text("Name of project"),
    n,
    Space(2),
    bbtn,
    bbbtn
    ])


#Code editor:




#Camera shader stuff
sh = None

def shin():
    camera.set_shader_input("blur_size", tslid.value)

def shader(shader):
    global sh
    if shader == "n":
        camera.shader = None
        sh = None
    if shader == "gray":
        camera.shader = camera_grayscale_shader
        sh = "grayscale"
    if shader == "blur":
        camera.shader = camera_vertical_blur_shader
        sh = "vertical blur"
tslid = ThinSlider(dynamic = True, on_value_changed = shin, max = .4, min = -.4, value = .15)
e = Button("close")
csm = WindowPanel(enabled = False, title = "Camera shader", content = [
    Button("No shader", on_click = Func(shader, "n")),
    Button("Camera grayscale shader", on_click = Func(shader, "gray")),
    Button("Camera vertical blur shader", on_click = Func(shader, "blur")),    tslid,
    e])
e.on_click = csm.disable
#loop

def update():
    global sh
    if sh == "vertical blur":
        tslid.enable()
    else:
        tslid.disable()
    csm.title = f'Camera shader'
    if held_keys["control"] and held_keys["b"]:
        bs.enable()
    if held_keys["control"] and held_keys["s"]:
        sv.enable()
    if held_keys["control"] and held_keys["o"]:
        lm.enable()
    if held_keys["control"] and held_keys["h"]:
        csm.enable()
    global entities, r_blist
    prev = len(r_bdict)
    for e in entitiesr:
        if e is not None:
            r_bdict[e.strmodel] = Func(gizmo,e)
    if prev != len(r_bdict):
        r_blist.disable()
        del r_blist
        r_blist = ButtonList(r_bdict, parent = r_panel, scale_x = 1, y = .4)

#Input loop
def input(key):
    if key == "c":
        exec(open("editor_main.py").read())
        



#Camera
EditorCamera()
app.run()
print("Exit")
sys.stdout = orgsts
print("Exit")
