# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 20:04:34 2017

@author: w9641432
"""
#from IPython import get_ipython
#get_ipython().magic('reset -sf')

import errno, stat, io
import os
import zipfile
import shutil
from distutils.dir_util import copy_tree


# Program that looks in fsx old ai directory and copies (and possibly changes) 
# bmp/dds files to new ai location. also, a new aircraft cfg is made by firstly creating
# a list of all new entries to be made. moveentry.py will move this to the new cfg
# a list of ac not found in the new directory is also made so manual installation
# can take place afterwards if new ac not avaialble, or say, a texture is missing. 


class MakeCFG: # class made to take in new variable names that are used to create the fltsim entry
    
    def __init__(self,new_src,new_dst,otitle,osim,omodel,otexture,oatc,oaticid,omanu,otype,ovar,odesc,ocode,opark):
      
      
      self.src = new_src
      self.dst = new_dst
      self.title = otitle
      self.sim = osim
      self.model = omodel
      self.texture = otexture
      self.airline = oatc
      self.atc_id = oatcid
      self.manufactorer = omanu
      self.type = otype
      self.variation = ovar
      self.description = odesc
      self.code = ocode
      self.parking = opark

      
    def writecfg(self):
        
         v = open(self.dst + "/" + "airplane.txt",'a')
         v.close()
         v = open(self.dst + "/" + "airplane.txt",'r')
         
         if v == []:
             
             v.write("[fltsim.0]" + "\n")
             
         else:
             v = open(self.dst + "/" + "airplane.txt",'r')
             lines = [line for line in v if line.strip()]
             fltsim= [t for t,x in enumerate(lines) if "[fltsim." in x]
             
             v.close()
             v = open(self.dst + "/" + "airplane.txt",'a')
             
             langd = len(fltsim)
             
             v.write("[fltsim." + str(langd) + "]" + "\n")
         
         if "\n" in self.title:
             v.write(self.title)
         else:
             v.write(self.title + "\n")
         
         if "\n" in self.sim:
             v.write(self.sim)
         else:
             v.write(self.sim + "\n")
             
         if "\n" in self.model:
             v.write(self.model)
         else:
             v.write(self.model + "\n")
             
         if "\n" in self.texture:
             v.write(self.texture)
         else:
             v.write(self.texture + "\n")
             
         v.write("sound=" + "\n")
         
         if "\n" in self.airline:
             v.write(self.airline)
         else:
             v.write(self.airline + "\n")
         
         if "\n" in self.atc_id:
             v.write(self.atc_id)
         else:
             v.write(self.atc_id + "\n")
             
         if "\n" in self.manufactorer:
             v.write(self.manufactorer)
         else:
             v.write(self.manufactorer + "\n")
             
         if "\n" in self.type:
             v.write(self.type)
         else:
             v.write(self.type + "\n")
             
         if "\n" in self.variation:
             v.write(self.variation)
         else:
             v.write(self.variation + "\n")    
         
         if "\n" in self.description:
             v.write(self.description)
         else:
             v.write(self.description + "\n")
         
         if "\n" in self.code:
             v.write(self.code)
         else:
             v.write(self.code + "\n")
         
         if "\n" in self.parking:
             v.write(self.parking)
         else:
             v.write(self.parking + "\n")   
         
         v.write("\n")
         
         v.close()
             
             
###########################abtkavapj#dg###################################################
my_park="atc_parking_codes=DHK,DHL"
my_type="atc_parking_types=CARGO"
airline='dhl'

#zippath = 'C:/Users/w9641432/Downloads/temp/'
zippath = 'C:/Users/w9641432/Desktop/fsx/downloads/'+ airline +'/'
z_out_path = 'C:/Users/w9641432/Desktop/fsx/temp/'
dst_ai = 'C:/Users/w9641432/Desktop/fsx/new_AI_Aircraft/'
items = os.listdir(zippath)

#shutil.rm('C:/Users/w9641432/Documents/Work/Python_learning/FSX2P3D/List of missing ac.txt')
#shutil.rm('C:/Users/w9641432/Documents/Work/Python_learning/FSX2P3D/List_of_installed_ac.txt')

g = open("List_of_installed_ac.txt",'a')
h = open("List of missing ac.txt",'a')

for i in range(0,len(items)):
    
    def handleRemoveReadonly(func, path, exc):
        excvalue = exc[1]
        if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
            os.chmod(z_out_path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
            func(path)
        else:
            raise
    if os.path.isdir(z_out_path):         

        if os.listdir(z_out_path) != []: # CHECKS THAT TEMP DIRECTORY IS EMPTY BEFORE UNZIPPING
            #os.mkdir(z_out_path,mode=0o777)         
            shutil.rmtree(z_out_path,ignore_errors=True, onerror=handleRemoveReadonly)
            os.mkdir(z_out_path,mode=0o777)
    else:
         
        os.mkdir(z_out_path,mode=0o777) 
   
    zip_ref = zipfile.ZipFile((zippath + items[i]), 'r')
    zip_ref.extractall(z_out_path)
    zip_contents = zip_ref.namelist()
    zip_ref.close() 
    
    contents = os.listdir(z_out_path)
    
    dir=z_out_path
    while len(contents) < 2:
        dir = dir + contents[0] + "/"
        contents = os.listdir(dir)
        
        
    zip_dir = dir + "/"
    print("Files to be considered: " + str(contents))    
    for j in range(0,len(contents)):
        if contents[j].endswith('.txt') or contents[j].endswith('.doc') or contents[j].endswith('.cfg'):
            
            f = open(zip_dir + contents[j],"r")
            lines = [line for line in f if line.strip()]
            
            # Check to see if it is in binary
            if "\x00" in lines:
                f.close()
                f = open(zip_dir + contents[j],"r",encoding="utf-16le")
                lines = [line for line in f if line.strip()]
            
            string= " ".join(str(x) for x in lines)
            f.close()
            if ("[fltsim." in string or "[FLTSIM." in string) and "sim=" in string and "title=" in string and "atc_airline=" in string:
                cfg_lines = lines
                break
            
        else:
            print("Cant find cfg entry in files")
            
            
                
    
    posi= [t for t,x in enumerate(cfg_lines) if "[fltsim" in x]
    yes = {'yes','y', 'ye', ''}
    no = {'no','n'}
    for k in range(0,len(posi)):
    
        choice = input("Install these textures? " + cfg_lines[posi[k]+1]).lower()

        if "y" in choice:
            
            if k >= len(posi)-1:
                    
                    cfg_sec = cfg_lines[posi[k]:]
            else:
                    cfg_sec = cfg_lines[posi[k]:posi[k+1]]
            
            
            if [t for t,x in enumerate(cfg_sec) if "title=" in x] != []:
                otitle= [t for t,x in enumerate(cfg_sec) if "title=" in x]
                otitle = cfg_sec[int(otitle[0])]
            else:
                otitle = "title= "
            
            if [t for t,x in enumerate(cfg_sec) if "sim=" in x] != []:
                osim= [t for t,x in enumerate(cfg_sec) if "sim=" in x]
                osim = cfg_sec[int(osim[0])]
            else:
                osim = "sim= "
                
            if [t for t,x in enumerate(cfg_sec) if "model=" in x] != []:
                omodel= [t for t,x in enumerate(cfg_sec) if "model=" in x]
                omodel = cfg_sec[int(omodel[0])]
            else:
                omodel = "model= "
                
            if "SL" in otitle or "Sl" in otitle or "sl" in otitle or "Sharklets" in otitle or "sharklets" in otitle or "Shark" in otitle or "Sharklet" in otitle or "sharklet" in otitle or "shark" in otitle:   
                omodel = omodel[:9] + "_S" + "\n"
                
            if [t for t,x in enumerate(cfg_sec) if "texture=" in x] !=[]:
                otexture = [t for t,x in enumerate(cfg_sec) if "texture=" in x]
                otexture = cfg_sec[int(otexture[0])]
            else:
                otexture = "texture= "
            
            if [t for t,x in enumerate(cfg_sec) if "atc_airline=" in x] != []:
                oatc = [t for t,x in enumerate(cfg_sec) if "atc_airline=" in x]
                oatc = cfg_sec[int(oatc[0])]
            else:
                oatc = "atc_airline= "
            
            if [t for t,x in enumerate(cfg_sec) if "atc_id=" in x] != []:
                oatcid = [t for t,x in enumerate(cfg_sec) if "atc_id=" in x]
                oatcid = cfg_sec[int(oatcid[0])]
            else:
                oatcid = "atc_id= "
            
            if [t for t,x in enumerate(cfg_sec) if "ui_manufacturer=" in x] != []:
                omanu = [t for t,x in enumerate(cfg_sec) if "ui_manufacturer=" in x]
                omanu = cfg_sec[int(omanu[0])]
            else:
                omanu = "ui_manufacturer= "
            
            if [t for t,x in enumerate(cfg_sec) if "ui_type=" in x] != []:
                ouitype = [t for t,x in enumerate(cfg_sec) if "ui_type=" in x]
                ouitype = cfg_sec[int(ouitype[0])]
            else:
                ouitype = "ui_type= "
            
            if [t for t,x in enumerate(cfg_sec) if "ui_variation=" in x] != []: 
                ouivar = [t for t,x in enumerate(cfg_sec) if "ui_variation=" in x]
                ouivar = cfg_sec[int(ouivar[0])]
            else:
                ouivar = "ui_variation= "
            
            if [t for t,x in enumerate(cfg_sec) if "description=" in x] != []:
                odesc = [t for t,x in enumerate(cfg_sec) if "description=" in x]
                odesc = cfg_sec[int(odesc[0])]
            else:
                odesc = "description= "
                
            if [t for t,x in enumerate(cfg_sec) if "atc_parking_codes=" in x] != []:
                o_code = [t for t,x in enumerate(cfg_sec) if "atc_parking_codes=" in x]
                o_code = cfg_sec[int(o_code[0])]
                if o_code.find(my_park) == 1:
                    o_code = "atc_parking_codes=" + o_code[18:-1] + ', ' + my_park[18:]
            else:
                o_code = my_park
            
            if [t for t,x in enumerate(cfg_sec) if "atc_parking_types=" in x] != []:
                o_type = [t for t,x in enumerate(cfg_sec) if "atc_parking_types=" in x]
                o_type = cfg_sec[int(o_type[0])] 
            else:
                o_type = my_type
            
# FSP             
                
            if "350900v1" in osim or "350900V1" in osim:
                new_dst = dst_ai + "AI_FSPX_A350-900/"
            
            elif "FSPXAI_MD11v1" in osim or "fspxai_md11v1" in osim or "FSPXAI_MD11V1" in osim or "Fspxai_Md11v1" in osim:
                new_dst = dst_ai + "AI_FSPX_MD11F_FSX/"
            
            elif "FSPXAI_B788v1" in osim or "fspxai_b788v1" in osim or "FSPXAI_B788V1" in osim or "Fspxai_b788v1" in osim:
                new_dst = dst_ai + "AI_FSPX_B787-8/"
                
            elif "FSPXAI_B789v1" in osim or "fspxai_b789v1" in osim or "FSPXAI_B789V1" in osim or "Fspxai_b789v1" in osim:
                new_dst = dst_ai + "AI_FSPX_B787-9/"    
# AIA                                
            elif "AIA_b717_t." in " ".join(str(x) for x in zip_contents) or "aia_b717_t" in " ".join(str(x) for x in zip_contents):
                new_dst = dst_ai + "AIA_717_FSX/"
                omodel = "model=no_refl"    
                
            elif "AIA_727_200" in osim or "aia_727_200" in osim:
                new_dst = dst_ai + "AIA_737_300v2_w_FSX/"
                if "727_100_t." in " ".join(str(x) for x in zip_contents):
                    omodel = "model=100"
                else:
                    omodel = "model=200"  
            
            elif "AIA_737_200" in osim or "aia_737_200" in osim:
                new_dst = dst_ai + "AIA_737_200_FSX/"
                omodel = "model=no_refl"
                
            elif "AIA_737_CL" in osim or "aia_737_CL" in osim:
                
                if "737_300_t." in " ".join(str(x) for x in zip_contents) or "737_300_T." in " ".join(str(x) for x in zip_contents):
                    if "733_w" in otitle or "733_W" in otitle or "733w" in otitle or "733W" in otitle or "737-300w" in otitle or "737-300W" in otitle or "Winglets" in otitle or "WINGLETS" in otitle or "winglets" in otitle or "BBJ" in otitle:
                        new_dst = dst_ai + "AIA_737_300v2_w_FSX/"
                        omodel = "model=300w"
                    else:
                        new_dst = dst_ai + "AIA_737_300v2_FSX/"
                        omodel = "model=300"
                elif "737_400_t." in " ".join(str(x) for x in zip_contents) or  "737_400_T." in " ".join(str(x) for x in zip_contents):
                    if "734_w" in otitle or "734_W" in otitle or "734w" in otitle or "734W" in otitle or "737-400w" in otitle or "737-400W" in otitle or "Winglets" in otitle or "WINGLETS" in otitle or "winglets" in otitle or "BBJ" in otitle:
                        new_dst = dst_ai + "AIA_737_400v2_w_FSX/"
                        omodel = "model=400w"
                    else:
                        new_dst = dst_ai + "AIA_737_400v2_FSX/"
                        omodel = "model=400"
                elif "737_500_t." in " ".join(str(x) for x in zip_contents) or "737_500_T." in " ".join(str(x) for x in zip_contents):
                    if "735_w" in otitle or "735_W" in otitle or "735w" in otitle or "735W" in otitle or "737-500w" in otitle or "737-500W" in otitle or "Winglets" in otitle or "WINGLETS" in otitle or "winglets" in otitle or "BBJ" in otitle:
                        new_dst = dst_ai + "AIA_737_500v2_w_FSX/"
                        omodel = "model=500w"
                    else:
                        new_dst = dst_ai + "AIA_737_500v2_FSX/"
                        omodel = "model=500"        
            
            elif "AIA_737_NG" in osim or "aia_737_NG" in osim:
                
                if "737_600_t." in " ".join(str(x) for x in zip_contents) or "737_600_T." in " ".join(str(x) for x in zip_contents):
                    new_dst = dst_ai + "AIA_737_600_FSX/"
                    omodel = "model=600"
                elif "737_700_t." in " ".join(str(x) for x in zip_contents) or "737_700_T." in " ".join(str(x) for x in zip_contents):
                    if "737_w" in otitle or "737_W" in otitle or "737w" in otitle or "737W" in otitle or "737-700w" in otitle or "737-700W" in otitle or "Winglets" in otitle or "WINGLETS" in otitle or "winglets" in otitle or "BBJ" in otitle:
                        new_dst = dst_ai + "AIA_737_700_W_FSX/"
                        omodel = "model=700w"
                    else:
                        new_dst = dst_ai + "AIA_737_700_FSX/"
                        omodel = "model=700"
                elif "737_800_t." in " ".join(str(x) for x in zip_contents) or "737_800_T." in " ".join(str(x) for x in zip_contents):
                    if "738_w" in otitle or "738_W" in otitle or "738w" in otitle or "738W" in otitle or "737-800w" in otitle or "737-800W" in otitle or "Winglets" in otitle or "WINGLETS" in otitle or "winglets" in otitle or "BBJ" in otitle:
                        new_dst = dst_ai + "AIA_737_800_W_FSX/"
                        omodel = "model=800w"
                    else:
                        new_dst = dst_ai + "AIA_737_800_FSX/"
                        omodel = "model=800"
                elif "737_900_t." in " ".join(str(x) for x in zip_contents) or "737_900_T." in " ".join(str(x) for x in zip_contents):
                    if "739_er" in otitle or "739_ER" in otitle or "739er" in otitle or "739ER" in otitle or "737-900er" in otitle or "737-900ER" in otitle or "Winglets" in otitle or "WINGLETS" in otitle or "winglets" in otitle or "739_w" in otitle or "739_W" in otitle or "739w" in otitle or "739W" in otitle or "737-900w" in otitle or "737-900W" in otitle:
                        new_dst = dst_ai + "AIA_737_900ER_FSX/"
                        omodel = "model=800w"
                    else:
                        new_dst = dst_ai + "AIA_737_900_FSX/"
                        omodel = "model=800"          
                             
            elif "AIA_747_200" in osim or "aia_747_200" in osim:
                new_dst = dst_ai + "AIA_727_200_PW_FSX/"
                omodel = "model="
               
            elif "AIA_747_300_C" in osim or "aia_747_300_c" in osim or "AIA_747_300_P" in osim or "aia_747_300_p" in osim or "AIA_747_300_R" in osim or "aia_747_300_r" in osim or "AIA_747_300" in osim or "aia_747_300" in osim:
                new_dst = dst_ai + "AIA_747_300_PW_FSX/"
                omodel = "model="
                if "rr_t." in " ".join(str(x) for x in zip_contents) or "RR_T." in " ".join(str(x) for x in zip_contents):
                    osim = "sim=aia_747_300_rr"
                elif "pw_t." in " ".join(str(x) for x in zip_contents) or "PW_T." in " ".join(str(x) for x in zip_contents):
                    osim = "sim=aia_747_300_pw"  
                elif "ge_t." in " ".join(str(x) for x in zip_contents) or "GE_T." in " ".join(str(x) for x in zip_contents):
                    osim = "sim=aia_747_300_cf6_50" 
                elif "d_t." in " ".join(str(x) for x in zip_contents)or "D_T." in " ".join(str(x) for x in zip_contents):
                    osim = "sim=aia_747_300_d"      
                
            elif "AIA_747_400_G" in osim or "aia_747_400_g" in osim or "AIA_747_400_P" in osim or "aia_747_400_p" in osim or "AIA_747_400_R" in osim or "aia_747_400_r" in osim or "AIA_747_400_D" in osim or "aia_747_400_d" in osim:
                new_dst = dst_ai + "AIA_747_400_GE_FSX/"
                omodel = "model="
                if "rr_t." in " ".join(str(x) for x in zip_contents):
                    osim = "sim=aia_747_400_rr.air"
                elif "pw_t." in " ".join(str(x) for x in zip_contents):
                    osim = "sim=aia_747_400_pw"  
                elif "ge_t." in " ".join(str(x) for x in zip_contents):
                    osim = "sim=aia_747_400_ge" 
                elif "d_t." in " ".join(str(x) for x in zip_contents):
                    osim = "sim=aia_747_400_d"     
                
            elif "AIA_747_400F" in osim or "aia_747_400f" in osim or "AIA_747_400f" in osim:
                new_dst = dst_ai + "AIA_747_400F_GE_FSX/"
                omodel = "model="
                osim = "sim=aia_747_400f"     
                
            elif "AIA_757_200_P" in osim or "aia_757_200_p" in osim or "AIA_757_200_R" in osim or "aia_757_200_r" in osim:
                new_dst = dst_ai + "AIA_757_200_RR_FSX/"
                omodel = "model="
                if "rr_t." in " ".join(str(x) for x in zip_contents) or "RR_T." in " ".join(str(x) for x in zip_contents):
                    osim = "sim=aia_757_200_rr"
                elif "pw_t." in " ".join(str(x) for x in zip_contents) or "PW_T." in " ".join(str(x) for x in zip_contents):
                    osim = "sim=aia_767_300_pw"     
                
            elif "AIA_757_200" in osim or "aia_757_200" in osim or "Aia_757_200" in osim:
                new_dst = dst_ai + "AIA_757_200w_RR_FSX/"
                omodel = "model="
                osim = "sim=aia_757_200"    
                
            elif "AIA_757_3" in osim or "aia_757_3" in osim or "Aia_757_3" in osim :
                new_dst = dst_ai + "AIA_757_300_RR_FSX/"
                omodel = "model="
                osim = "sim=aia_757_300_rr"
            
            elif "AIA_767_2" in osim or "aia_767_2" in osim or "AIA_767_2" in osim:
                new_dst = dst_ai + "AIA_767_200_GE_FSX/"
                omodel = "model=762"
                if "ge_t." in " ".join(str(x) for x in zip_contents) or "GE_T." in " ".join(str(x) for x in zip_contents):
                    osim = "sim=aia_767_300_ge"
                elif "pw_t." in " ".join(str(x) for x in zip_contents) or "PW_T." in " ".join(str(x) for x in zip_contents):
                    osim = "sim=aia_767_300_pw" 
            
            elif "AIA_767_300_GE" in osim or "aia_767_300_ge" in osim or "AIA_767_300_ge" in osim or "aia_767_300_GE" in osim or "AIA_767_300_PW" in osim or "aia_767_300_pw" in osim or "AIA_767_300_pw" in osim or "aia_767_300_PW" in osim or "AIA_767_300_RR" in osim or "aia_767_300_rr" in osim or "AIA_767_300_rr" in osim or "aia_767_300_RR" in osim:
                new_dst = dst_ai + "AIA_767_300_GE_FSX/"
                if "ge_t." in " ".join(str(x) for x in zip_contents) or "GE_T." in " ".join(str(x) for x in zip_contents):
                    omodel = "model=GE_no_refl"
                    osim = "sim=aia_767_300_ge" 
                elif "pw_t." in " ".join(str(x) for x in zip_contents) or "PW_T." in " ".join(str(x) for x in zip_contents):
                    omodel = "model=GE_no_refl"
                    osim = "sim=aia_767_300_pw" 
                elif "rr_t." in " ".join(str(x) for x in zip_contents) or "RR_T." in " ".join(str(x) for x in zip_contents):
                    omodel = "model=GE_no_refl"
                    osim = "sim=aia_767_300_rr" 
                
            elif "AIA_767_300_W" in osim or "aia_767_300_w" in osim or "AIA_767_300_w" in osim or "AIA_767_300w" in osim or "aia_767_300w" in osim or "AIA_767_300W" in osim or '767-300w' in ouitype or '767-300W' in ouitype or '763w' in ouitype or '763W' in ouitype:
                new_dst = dst_ai + "AIA_767_300_W/"
                osim = "sim=aia_767_300w" 
                if "ge_t." in " ".join(str(x) for x in zip_contents) or "GE_T." in " ".join(str(x) for x in zip_contents):
                    omodel = "model=GE_no_refl"
                elif "pw_t." in " ".join(str(x) for x in zip_contents) or "PW_T." in " ".join(str(x) for x in zip_contents):
                    omodel = "model=PW_no_refl" 
                    
            elif "AIA_767_4" in osim or "aia_767_4" in osim or "AIA_767_4" in osim:
                new_dst = dst_ai + "AIA_767_400_GE_FSX/"
                osim = "sim=aia_767_400" 
                if "ge_t." in " ".join(str(x) for x in zip_contents) or "GE_T." in " ".join(str(x) for x in zip_contents):
                    omodel = "model="
                elif "pw_t." in " ".join(str(x) for x in zip_contents) or "PW_T." in " ".join(str(x) for x in zip_contents):
                    omodel = "model="            
                    
            elif "AIA_DC_9_30" in osim or "aia_dc_9_30" in osim:
                new_dst = dst_ai + "AIA_DC_9_30_FSX/"
                omodel = "model="
            elif "AIA_DC_9_50" in osim or "aia_dc_9_50" in osim:
                new_dst = dst_ai + "AIA_DC_9_50_FSX/" 
                omodel = "model="
            elif "AIA_EMB_120" in osim or "aia_emb_120" in osim:
                new_dst = dst_ai + "AIA_EMB120_FSX/"
                omodel = "model="
            elif "AIA_EMB_170" in osim or "aia_emb_170" in osim:
                new_dst = dst_ai + "AIA_EMB170_FSX/"
                omodel = "model="
            elif "AIA_EMB_175" in osim or "aia_emb_175" in osim:
                new_dst = dst_ai + "AIA_EMB175_FSX/"
                omodel = "model="
            elif "AIA_EMB190" in osim or "aia_emb190" in osim:
                new_dst = dst_ai + "AIA_EMB190_FSX/"     
                omodel = "model="
            elif "AIA_EMB195" in osim or "aia_emb195" in osim:
                new_dst = dst_ai + "AIA_EMB195_FSX/" 
                omodel = "model="
            elif "AIA_EMB195" in osim or "aia_emb195" in osim:
                new_dst = dst_ai + "AIA_EMB195_FSX/"     
                omodel = "model="
            elif "AIA_FOKKER_70" in osim or "aia_fokker_70" in osim or "aia_Fokker_70" in osim or "AIA_Fokker_70" in osim:
                new_dst = dst_ai + "AIA_Fokker_70_FSX/"     
                omodel = "model="
            elif "AIA_FOKKER_100" in osim or "aia_fokker_100" in osim or "aia_Fokker_100" in osim or "AIA_Fokker_100" in osim:
                new_dst = dst_ai + "AIA_Fokker_100_FSX/"     
                omodel = "model=" 
            
            elif "md8x_t." in " ".join(str(x) for x in zip_contents) or "MD8X_T." in " ".join(str(x) for x in zip_contents):
                new_dst = dst_ai + "AIA_MD_80_FSX/"     
                omodel = "model="
                osim = "sim=aia_MD_8X"
            elif "md87_t." in " ".join(str(x) for x in zip_contents) or "MD87_T." in " ".join(str(x) for x in zip_contents):
                new_dst = dst_ai + "AIA_MD_87_FSX/"     
                omodel = "model=" 
                osim = "sim=aia_MD_8X"
            elif "md90_t." in " ".join(str(x) for x in zip_contents) or "MD90_T." in " ".join(str(x) for x in zip_contents):
                new_dst = dst_ai + "AIA_MD_90_FSX/"     
                omodel = "model=" 
                osim = "sim=aia_MD_8X" 
# AIG                
            elif "AIG_753" in osim or "aig_753" in osim or "aig_753" in osim:
                new_dst = dst_ai + "AIG_757-300W/"     
                
                if "AIG_B753_RR." in " ".join(str(x) for x in zip_contents) or "aig_b753_rr." in " ".join(str(x) for x in zip_contents):
                    omodel = "model=RR_WL" 
                else:
                    omodel = "model=PW_WL"
            
            elif "AIG_752" in osim or "Aig_752" in osim or "aig_752" in osim:
                new_dst = dst_ai + "AIG_757-200/"     
                
                if "752_w" in otitle or "752_W" in otitle or "752w" in otitle or "752W" in otitle or "757-200w" in otitle or "757-200W" in otitle or "Winglets" in otitle or "WINGLETS" in otitle or "winglets" in otitle:
 
                    if "AIG_B752_RR." in " ".join(str(x) for x in zip_contents) or "aig_b752_rr." in " ".join(str(x) for x in zip_contents):
                        omodel = "model=RR_WL" 
                    else:
                        omodel = "model=PW_WL"
                else:
                    if "AIG_B752_RR." in " ".join(str(x) for x in zip_contents) or "aig_b752_rr." in " ".join(str(x) for x in zip_contents):
                        omodel = "model=RR" 
                    else:
                        omodel = "model=PW"
            
            elif "AIG_CRJ700" in osim or "aig_crj700" in osim or "AIG_crj700" in osim or "AIG_Crj700" in osim:
                new_dst = dst_ai + "AIG_CRJ-700/"     
                omodel = "model="
            
            elif "AIG_CRJ900" in osim or "aig_crj900" in osim or "AIG_crj900" in osim or "AIG_Crj900" in osim:
                new_dst = dst_ai + "AIG_CRJ-900/"     
                omodel = "model="
                
            elif "AIG_328_300" in osim or "aig_328_300" in osim or "Aig_328_300" in osim:
                new_dst = dst_ai + "AIG_D328_300_JET/"     
                omodel = "model="    
# FAIB                
            elif "FAIB_A318" in osim or "faib_a318" in osim:
                
                if "CFM_S" in omodel or "cfm_S" in omodel or "cfm_s" in omodel or "cfmc_s" in omodel or "CFMC_S" in omodel:
                    new_dst = dst_ai + "FAIB_A318S_CFM/"
                    omodel = "model=CFM_S"
                elif "CFM" in omodel or "CFMC" in omodel or "cfm" in omodel or "cfmc" in omodel or "cfmC" in omodel:
                    new_dst = dst_ai + "FAIB_A318_CFM/"
                    omodel = "model=CFM"
                elif "PW_S" in omodel or "pw_s" in omodel:
                    new_dst = dst_ai + "FAIB_A318S_PW/" 
                    omodel = "model=PW_S"    
                elif "PW" in omodel or "pw" in omodel:
                    new_dst = dst_ai + "FAIB_A318_PW/"
                    omodel = "model=PW"
                
            
            elif "FAIB_A319" in osim or "faib_a319" in osim:
                
                if "CFM_S" in omodel or "cfm_S" in omodel or "cfm_s" in omodel or "cfmc_s" in omodel or "CFMC_S" in omodel or 'sharkets' in otitle or 'SHARKLETS' in otitle or 'Sharklet' in otitle or 'sharklet' in otitle or 'SHARKLET' in otitle or 'SL' in otitle or 'A319S' in otitle or 'a319s' in otitle or 'SL' in otexture or 'sl' in otexture:
                    new_dst = dst_ai + "FAIB_A319S_CFM/"
                    omodel = "model=CFM_S"
                elif "CFM" in omodel or "CFMC" in omodel or "cfm" in omodel or "cfmc" in omodel or "cfmC" in omodel:
                    new_dst = dst_ai + "FAIB_A319_CFM/"
                    omodel = "model=CFM"
                elif "IAE_S" in omodel or "iae_s" in omodel or 'sharkets' in otitle or 'SHARKLETS' in otitle or 'Sharklet' in otitle or 'sharklet' in otitle or 'SHARKLET' in otitle or 'SL' in otitle or 'A319S' in otitle or 'a319s' in otitle or 'SL' in otexture or 'sl' in otexture:
                    new_dst = dst_ai + "FAIB_A319S_IAE/" 
                    omodel = "model=IAE_S" 
                elif "IAE" in omodel or "iae" in omodel:
                    new_dst = dst_ai + "FAIB_A319_IAE/"
                    omodel = "model=IAE"
                
                    
            elif "FAIB_A320" in osim or "faib_a320" in osim:
                
                if "CFM_S" in omodel or "cfm_S" in omodel or "cfm_s" in omodel or "cfmc_s" in omodel or "CFMC_S" in omodel  or 'Sharkets' in otitle or 'sharkets' in otitle or 'SHARKLETS' in otitle or 'Sharklet' in otitle or 'sharklet' in otitle or 'SHARKLET' in otitle or 'SL' in otitle or 'A320S' in otitle or 'a320s' in otitle or 'SL' in otexture or 'sl' in otexture or '200sl' in otitle or '200SL' in otitle or '200sl' in otitle or '200SL' in otitle:
                    new_dst = dst_ai + "FAIB_A320S_CFM/"
                    omodel = "model=CFM_S"
                elif "CFM" in omodel or "CFMC" in omodel or "cfm" in omodel or "cfmc" in omodel or "cfmC" in omodel:
                    new_dst = dst_ai + "FAIB_A320_CFM/"
                    omodel = "model=CFM"
                elif "IAE_S" in omodel or "iae_s" in omodel or 'Sharkets' in otitle or 'sharkets' in otitle or 'SHARKLETS' in otitle or 'Sharklet' in otitle or 'sharklet' in otitle or 'SHARKLET' in otitle or 'SL' in otitle or 'A320S' in otitle or 'a320s' in otitle or 'SL' in otexture or 'sl' in otexture or '200sl' in otitle or '200SL' in otitle or '200sl' in otitle or '200SL' in otitle:
                    new_dst = dst_ai + "FAIB_A320S_IAE/" 
                    omodel = "model=IAE_S"     
                elif "IAE_DB" in omodel or "iae_db" in omodel:
                    new_dst = dst_ai + "FAIB_A320_IAE_DB/"
                    omodel = "model=IAE_DB"    
                elif "IAE" in omodel or "iae" in omodel:
                    new_dst = dst_ai + "FAIB_A320_IAE/"
                    omodel = "model=IAE"        
                    
            elif "FAIB_A321" in osim or "faib_a321" in osim:
                
                if "CFM_S" in omodel or "cfm_S" in omodel or "cfm_s" in omodel or "cfmc_s" in omodel or "CFMC_S" in omodel or 'sharkets' in otitle or 'SHARKLETS' in otitle or 'Sharklet' in otitle or 'sharklet' in otitle or 'SHARKLET' in otitle or 'SL' in otitle or 'A321S' in otitle or 'a321s' in otitle or 'SL' in otexture or 'sl' in otexture:
                    new_dst = dst_ai + "FAIB_A321S_CFM/"
                    omodel = "model=CFM_S"
                elif "CFM" in omodel or "CFMC" in omodel or "cfm" in omodel or "cfmc" in omodel or "cfmC" in omodel:
                    new_dst = dst_ai + "FAIB_A321_CFM/"
                    omodel = "model=CFM" 
                elif "IAE_S" in omodel or "iae_s" in omodel or 'sharkets' in otitle or 'SHARKLETS' in otitle or 'Sharklet' in otitle or 'sharklet' in otitle or 'SHARKLET' in otitle or 'SL' in otitle or 'A321S' in otitle or 'a321s' in otitle or 'SL' in otexture or 'sl' in otexture or 'SL' in otexture or 'sl' in otexture:
                    new_dst = dst_ai + "FAIB_A321S_IAE/" 
                    omodel = "model=IAE_S" 
                elif "IAE" in omodel or "iae" in omodel:
                    new_dst = dst_ai + "FAIB_A321_IAE/"
                    omodel = "model=IAE"    
            
            elif "FAIB_7372" in osim or "faib_7372" in osim:
                if "gravelnormal" in omodel or "normal" in omodel or "Gravelnormal" in omodel or "Normal" in omodel or "GRAVELNORMAL" in omodel or "NORMAL" in omodel:
                    new_dst = dst_ai + "FAIB_B737-200_N/"
                elif "gravellogolight" in omodel or "logolight" in omodel or "Gravellogolight" in omodel or "Logolight" in omodel or "GRAVELLOGOLIGHT" in omodel or "LOGOLIGHT" in omodel:
                    new_dst = dst_ai + "FAIB_B737-200_L/"    
                     
            elif "FAIB_7373" in osim or "faib_7373" in osim:
                if "logolight" in omodel or "Logolight" in omodel or "LOGOLIGHT" in omodel:
                    new_dst = dst_ai + "FAIB_B737-300_L/"
                elif "normal" in omodel or "Normal" in omodel or "NORMAL" in omodel:
                    new_dst = dst_ai + "FAIB_B737-300_N/" 
                elif "winglets" in omodel or "Winglets" in omodel or "WINGLETS" in omodel:
                    new_dst = dst_ai + "FAIB_B737-300_W/" 
            
            elif "FAIB_7374" in osim or "faib_7374" in osim:
                if "logolight" in omodel or "Logolight" in omodel or "LOGOLIGHT" in omodel:
                    new_dst = dst_ai + "FAIB_B737-400_L/"
                elif "normal" in omodel or "Normal" in omodel or "NORMAL" in omodel:
                    new_dst = dst_ai + "FAIB_B737-400_N/" 
                elif "winglets" in omodel or "Winglets" in omodel or "WINGLETS" in omodel:
                    new_dst = dst_ai + "FAIB_B737-400_W/" 
                    
            elif "FAIB_7375" in osim or "faib_7375" in osim:
                if "logolight" in omodel or "Logolight" in omodel or "LOGOLIGHT" in omodel:
                    new_dst = dst_ai + "FAIB_B737-500_L/"
                elif "normal" in omodel or "Normal" in omodel or "NORMAL" in omodel:
                    new_dst = dst_ai + "FAIB_B737-500_N/" 
                elif "winglets" in omodel or "Winglets" in omodel or "WINGLETS" in omodel:
                    new_dst = dst_ai + "FAIB_B737-500_W/" 
                    
            elif "FAIB_7376" in osim or "faib_7376" in osim:
                if "scimitars_SN" in omodel or "Scimitars_SN" in omodel or "scimitars_sn" in omodel or "SCIMITARS_SN" in omodel:
                    new_dst = dst_ai + "FAIB_B737-600_W/"
                    omodel = "model=scimitars_SN"
                elif "scimitars" in omodel or "Scimitars" in omodel or "SCIMITARS" in omodel:
                    new_dst = dst_ai + "FAIB_B737-600_W/"
                    omodel = "model=scimitars"
                elif "winglets" in omodel or "Winglets" in omodel or "WINGLETS" in omodel:
                    new_dst = dst_ai + "FAIB_B737-600_W/"
                    omodel = "model=winglets"
                elif "winglets_SN" in omodel or "Winglets_SN" in omodel or "winglets_sn" in omodel or "WINGLETS_SN" in omodel:
                    new_dst = dst_ai + "FAIB_B737-600_W/"
                    omodel = "model=winglets_SN"
                elif "SN" in omodel or "Sn" in omodel or "sn" in omodel:
                    new_dst = dst_ai + "FAIB_B737-600/"
                else:    
                    new_dst = dst_ai + "FAIB_B737-600/"
                    omodel="model="
                    
            elif "FAIB_7377" in osim or "faib_7377" in osim:
                
                if "scimitars_SN" in omodel or "Scimitars_SN" in omodel or "scimitars_sn" in omodel or "SCIMITARS_SN" in omodel:
                    new_dst = dst_ai + "FAIB_B737-700_W/"
                    omodel = "model=scimitars_SN"
                elif "scimitars" in omodel or "Scimitars" in omodel or "SCIMITARS" in omodel:
                    new_dst = dst_ai + "FAIB_B737-700_W/"
                    omodel = "model=scimitars"
                elif "winglets" in omodel or "Winglets" in omodel or "WINGLETS" in omodel:
                    new_dst = dst_ai + "FAIB_B737-700_W/"
                    omodel = "model=winglets"
                elif "winglets_SN" in omodel or "Winglets_SN" in omodel or "winglets_sn" in omodel or "WINGLETS_SN" in omodel:
                    new_dst = dst_ai + "FAIB_B737-700_W/"
                    omodel = "model=winglets_SN"
                elif "SN" in omodel or "Sn" in omodel or "sn" in omodel:
                    new_dst = dst_ai + "FAIB_B737-700/"    
                else:    
                    new_dst = dst_ai + "FAIB_B737-700/"
                    omodel="model="
                    
            elif "FAIB_7378" in osim or "faib_7378" in osim:
               
                if "scimitars_SN" in omodel or "Scimitars_SN" in omodel or "scimitars_sn" in omodel or "SCIMITARS_SN" in omodel:
                    new_dst = dst_ai + "FAIB_B737-800_W/"
                    omodel = "model=scimitars_SN"
                elif "scimitars" in omodel or "Scimitars" in omodel or "SCIMITARS" in omodel:
                    new_dst = dst_ai + "FAIB_B737-800_W/"
                    omodel = "model=scimitars"
                elif "winglets" in omodel or "Winglets" in omodel or "WINGLETS" in omodel:
                    new_dst = dst_ai + "FAIB_B737-800_W/"
                    omodel = "model=winglets"
                elif "winglets_SN" in omodel or "Winglets_SN" in omodel or "winglets_sn" in omodel or "WINGLETS_SN" in omodel:
                    new_dst = dst_ai + "FAIB_B737-800_W/"
                    omodel = "model=winglets_SN"
                elif "SN" in omodel or "Sn" in omodel or "sn" in omodel:
                    new_dst = dst_ai + "FAIB_B737-800/"    
                else:    
                    new_dst = dst_ai + "FAIB_B737-800/"
                    omodel="model="  
                    
            elif "FAIB_7379" in osim or "faib_7379" in osim:
                
                if "scimitars_SN" in omodel or "Scimitars_SN" in omodel or "scimitars_sn" in omodel or "SCIMITARS_SN" in omodel:
                    new_dst = dst_ai + "FAIB_B737-900_W/"
                    omodel = "model=scimitars_SN"
                elif "scimitars" in omodel or "Scimitars" in omodel or "SCIMITARS" in omodel:
                    new_dst = dst_ai + "FAIB_B737-900_W/"
                    omodel = "model=scimitars"
                elif "winglets" in omodel or "Winglets" in omodel or "WINGLETS" in omodel:
                    new_dst = dst_ai + "FAIB_B737-900_W/"
                    omodel = "model=winglets"
                elif "winglets_SN" in omodel or "Winglets_SN" in omodel or "winglets_sn" in omodel or "WINGLETS_SN" in omodel:
                    new_dst = dst_ai + "FAIB_B737-900_W/"
                    omodel = "model=winglets_SN"
                elif "SN" in omodel or "Sn" in omodel or "sn" in omodel:
                    new_dst = dst_ai + "FAIB_B737-900/"    
                else:    
                    new_dst = dst_ai + "FAIB_B737-900/"
                    omodel="model="  
                    
            elif "FAIB_7478F" in osim or "faib_7478f" in osim:
                
                if "fNWF" in omodel or "FNWF" in omodel or "fnwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-8F/"
                    omodel = "model=fNWF"
                elif "f" in omodel or "F" in omodel:
                    new_dst = dst_ai + "FAIB_B747-8F/"
                    omodel = "model=f"    
                    
            elif "FAIB_7478" in osim or "faib_7478" in osim:
                if "NWF" in omodel or "Nwf" in omodel or "nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-8/"
                    omodel = "model=NWF" 
                elif "f" in omodel or "F" in omodel:
                    new_dst = dst_ai + "FAIB_B747-8/"
                    omodel = "model="
                       
            elif "FAIB_7471" in osim or "faib_7471" in osim:
                if "NWF" in omodel or "Nwf" in omodel or "nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-100/"
                    omodel = "model=NWF" 
                    
            elif "FAIB_747-200_GE" in osim or "faib_747-200_ge" in osim:
                if "GENR_NWF" in omodel or "genr_nwf" in omodel or "genr_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-200_GE/"
                    omodel = "model=GENR_NWF"
                elif "GE_NWF" in omodel or "GE_nwf" in omodel or "ge_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-200_GE/"
                    omodel = "model=GE_NWF"
                elif "GENR" in omodel or "GEnr" in omodel or "genr" in omodel:
                    new_dst = dst_ai + "FAIB_B747-200_GE/"
                    omodel = "model=GENR" 
                else:
                    new_dst = dst_ai + "FAIB_B747-200_GE/"
                    omodel = "model=GE"    
            
            elif "FAIB_747-200_PW" in osim or "faib_747-200_pw" in osim:
                if "PWNR_NWF" in omodel or "PWnr_nwf" in omodel or "pwnr_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-200_PW/"
                    omodel = "model=PWNR_NWF"
                elif "PW_NWF" in omodel or "PW_nwf" in omodel or "pw_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-200_PW/"
                    omodel = "model=PW_NWF"
                elif "PWNR" in omodel or "PWnr" in omodel or "pwnr" in omodel:
                    new_dst = dst_ai + "FAIB_B747-200_PW/"
                    omodel = "model=PWNR" 
                else:
                    new_dst = dst_ai + "FAIB_B747-200_PW/"
                    omodel = "model=PW" 
                    
            elif "FAIB_747-200_RR" in osim or "faib_747-200_rr" in osim:
                if "RRNR_NWF" in omodel or "RRnr_nwf" in omodel or "rrnr_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-200_PW/"
                    omodel = "model=RRNR_NWF"
                elif "RR_NWF" in omodel or "RR_nwf" in omodel or "rr_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-200_PW/"
                    omodel = "model=RR_NWF"
                elif "RRNR" in omodel or "RRnr" in omodel or "rrnr" in omodel:
                    new_dst = dst_ai + "FAIB_B747-200_RR/"
                    omodel = "model=RRNR" 
                else:
                    new_dst = dst_ai + "FAIB_B747-200_RR/"
                    omodel = "model=RR"         
            
            elif "FAIB_747-300_GE" in osim or "faib_747-300_ge" in osim:
                if "GE80NR_NWF" in omodel or "GE80nr_nwf" in omodel or "ge80nr_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-300_GE/"
                    omodel = "model=GE80NR_NWF"
                elif "GE80_NWF" in omodel or "GE80_nwf" in omodel or "ge80_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-300_GE/"
                    omodel = "model=GE80_NWF"
                elif "GE80NR" in omodel or "GE80nr" in omodel or "ge80nr" in omodel:
                    new_dst = dst_ai + "FAIB_B747-300_GE/"
                    omodel = "model=GE80NR" 
                elif "GE80" in omodel or "ge80" in omodel:
                    new_dst = dst_ai + "FAIB_B747-300_GE/"
                    omodel = "model=GE80"  
                elif "GE50NR_NWF" in omodel or "GE50nr_nwf" in omodel or "ge50nr_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-300_GE/"
                    omodel = "model=GE50NR_NWF"
                elif "GE50_NWF" in omodel or "GE50_nwf" in omodel or "ge50_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-300_GE/"
                    omodel = "model=GE50_NWF"
                elif "GE50NR" in omodel or "GE50nr" in omodel or "ge50nr" in omodel:
                    new_dst = dst_ai + "FAIB_B747-300_GE/"
                    omodel = "model=GE50NR" 
                elif "GE50" in omodel or "ge50" in omodel:
                    new_dst = dst_ai + "FAIB_B747-300_GE/"
                    omodel = "model=GE50"
                    
            elif "FAIB_747-300_PW" in osim or "faib_747-300_pw" in osim:
                if "PWNR_NWF" in omodel or "PWnr_nwf" in omodel or "pwnr_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-300_PW/"
                    omodel = "model=PWNR_NWF"
                elif "PW_NWF" in omodel or "PW_nwf" in omodel or "pw_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-300_PW/"
                    omodel = "model=PW_NWF"
                elif "PWNR" in omodel or "PWnr" in omodel or "pwnr" in omodel:
                    new_dst = dst_ai + "FAIB_B747-300_PW/"
                    omodel = "model=PWNR" 
                else:
                    new_dst = dst_ai + "FAIB_B747-300_PW/"
                    omodel = "model=PW" 
                    
            elif "FAIB_747-300_RR" in osim or "faib_747-300_rr" in osim:
                if "RRNR_NWF" in omodel or "RRnr_nwf" in omodel or "rrnr_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-300_PW/"
                    omodel = "model=RRNR_NWF"
                elif "RR_NWF" in omodel or "RR_nwf" in omodel or "rr_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-300_PW/"
                    omodel = "model=RR_NWF"
                elif "RRNR" in omodel or "RRnr" in omodel or "rrnr" in omodel:
                    new_dst = dst_ai + "FAIB_B747-300_RR/"
                    omodel = "model=RRNR" 
                else:
                    new_dst = dst_ai + "FAIB_B747-300_RR/"
                    omodel = "model=RR" 
                    
             
            elif "FAIB_7474D" in osim or "faib_7474d" in osim:
                if "DGE_NWF" in omodel or "DGE_Nwf" in omodel or "dge_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400D_GE/"
                    omodel = "model=DGE_NWF"
                else:
                    new_dst = dst_ai + "FAIB_B747-400D_GE/"
                    omodel = "model=DGE"
                    
            elif "FAIB_7474F" in osim or "faib_7474f" in osim:
                if "FGE_NWF" in omodel or "FGE_Nwf" in omodel or "FGE_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400F_GE/"
                    omodel = "model=FGE_NWF"
                elif "FGE" in omodel or "Fge" in omodel or "fge" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400F_GE/"
                    omodel = "model=FGE" 
                elif "FPW_NWF" in omodel or "FPW_Nwf" in omodel or "fpw_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400F_PW/"
                    omodel = "model=FPW_NWF"
                elif "FPW" in omodel or "Fpw" in omodel or "fpw" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400F_PW/"
                    omodel = "model=FPW"         
                elif "FRR_NWF" in omodel or "FRR_Nwf" in omodel or "frr_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400F_RR/"
                    omodel = "model=FRR_NWF"
                elif "FRR" in omodel or "Frr" in omodel or "frr" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400F_RR/"
                    omodel = "model=FRR"
                    
            elif "FAIB_B7474SP" in osim or "faib_7474sp" in osim:
                if "PW_NWF" in omodel or "PW_Nwf" in omodel or "pw_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400SP_PW/"
                    omodel = "model=PW_NWF"
                elif "PW" in omodel or "Pw" in omodel or "pw" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400SP_PW/"
                    omodel = "model=PW" 
                elif "RR_NWF" in omodel or "RR_Nwf" in omodel or "rr_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400SP_RR/"
                    omodel = "model=RR_NWF"
                elif "RR" in omodel or "Rr" in omodel or "rr" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400SP_RR/"
                    omodel = "model=RR"   
                    
            elif "FAIB_7474" in osim or "faib_7474" in osim:
                if "GE_NWF" in omodel or "GE_Nwf" in omodel or "ge_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400_GE/"
                    omodel = "model=GE_NWF"
                elif "GE" in omodel or "Ge" in omodel or "ge" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400_GE/"
                    omodel = "model=GE"
                elif "PW_NWF" in omodel or "PW_Nwf" in omodel or "pw_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400_PW/"
                    omodel = "model=PW_NWF"
                elif "PW" in omodel or "Pw" in omodel or "pw" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400_PW/"
                    omodel = "model=PW"        
                elif "RR_NWF" in omodel or "RR_nwf" in omodel or "rr_nwf" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400_RR/"
                    omodel = "model=RR_NWF"
                elif "RR" in omodel or "Rr" in omodel or "rr" in omodel:
                    new_dst = dst_ai + "FAIB_B747-400_RR/"
                    omodel = "model=RR"
                           
# OSP       
            elif "ATR42" in osim or "atr42" in osim:
                if "300" in omodel:
                    new_dst = dst_ai + "OSP_ATR 42-300/"
                    omodel = "model=300P3Dv4"
                    #omodel = "model=300FSX"
                elif "400" in omodel:
                    new_dst = dst_ai + "OSP_ATR 42-400/"
                    omodel = "model=400P3Dv4"
                    #omodel = "model=400FSX"
                elif "500" in omodel:
                    new_dst = dst_ai + "OSP_ATR 42-500/"
                    omodel = "model=500P3Dv4"
                    #omodel = "model=500FSX"
                    
            elif "ATR72" in osim or "atr72" in osim:
                if "200" in omodel:
                    new_dst = dst_ai + "OSP_ATR 72-200/"
                    omodel = "model=P3Dv4"
                    #omodel = "model=300FSX"
                elif "210" in omodel:
                    new_dst = dst_ai + "OSP_ATR 72-210/"
                    omodel = "model=P3Dv4"
                    #omodel = "model=400FSX"
                elif "500" in omodel:
                    new_dst = dst_ai + "OSP_ATR 72-500/"
                    omodel = "model=P3Dv4"
                elif "600" in omodel:
                    new_dst = dst_ai + "OSP_ATR 72-500/"
                    omodel = "model=P3Dv4"    
                    #omodel = "model=500FSX"         
# TFS
            elif "_A300" in osim or "_a300" in osim:
                if "A30B_GE" in omodel or "a30b_ge" in omodel or "a30b_GE" in omodel or "A30B_ge" in omodel:
                    new_dst = dst_ai + "TFS_A300-600/"
                    omodel = "model=A30B_GE"
                elif "A30B_PW" in omodel or "a30b_pw" in omodel or "a30b_PW" in omodel or "A30B_pw" in omodel:
                    new_dst = dst_ai + "TFS_A300-600/"
                    omodel = "model=A30B_PW"
                elif "A306_PW" in omodel or "a306_pw" in omodel:
                    new_dst = dst_ai + "TFS_A300-600/"
                    omodel = "model=A306_PW"
                elif "A306_GE" in omodel or "a306_ge" in omodel:
                    new_dst = dst_ai + "TFS_A300-600/"
                    omodel = "model=A306_GE"     

            elif "_A310" in osim or "_a310" in osim:
                if "GE_200" in omodel or "ge_200" in omodel:
                    new_dst = dst_ai + "TFS_A310/"
                    omodel = "model=GE_200"
                elif "GE_300" in omodel or "ge_300" in omodel :
                    new_dst = dst_ai + "TFS_A310/"
                    omodel = "model=GE_300"
                elif "PW_200" in omodel or "pw_200" in omodel:
                    new_dst = dst_ai + "TFS_A310/"
                    omodel = "model=PW_200"
                elif "PW_300" in omodel or "pw_300" in omodel :
                    new_dst = dst_ai + "TFS_A310/"
                    omodel = "model=PW_300" 
            
            elif "_A332F" in osim or "_a332f" in osim:
                if "RR" in omodel or "rr" in omodel:
                    new_dst = dst_ai + "TFS_A330-200F/"
                    omodel = "model=RR"
                elif "PW" in omodel or "pw" in omodel:
                    new_dst = dst_ai + "TFS_A330-200F/"
                    omodel = "model=PW"
            
            elif "_A332" in osim or "_a332" in osim:
                if "RR" in omodel or "rr" in omodel:
                    new_dst = dst_ai + "TFS_A330-200/"
                    omodel = "model=RR"
                elif "GE" in omodel or "ge" in omodel :
                    new_dst = dst_ai + "TFS_A330-200/"
                    omodel = "model=GE"
                elif "PW" in omodel or "pw" in omodel:
                    new_dst = dst_ai + "TFS_A330-200/"
                    omodel = "model=PW"
            
            elif "_A333" in osim or "_a333" in osim:
                if "RR" in omodel or "rr" in omodel:
                    new_dst = dst_ai + "TFS_A330-300/"
                    omodel = "model=RR"
                elif "GE" in omodel or "ge" in omodel :
                    new_dst = dst_ai + "TFS_A330-300/"
                    omodel = "model=GE"
                elif "PW" in omodel or "pw" in omodel:
                    new_dst = dst_ai + "TFS_A330-300/"
                    omodel = "model=PW"

            elif "_A342" in osim or "_a342" in osim:
                new_dst = dst_ai + "TFS_A340-200/"
                omodel = "model="

            elif "_A343" in osim or "_a343" in osim:
                if "Normal" in omodel or "normal" in omodel or "NORMAL" in omodel:
                    new_dst = dst_ai + "TFS_A340-300/"
                    omodel = "model=Normal"
                elif "GE" in omodel or "ge" in omodel :
                    new_dst = dst_ai + "TFS_A340-300/"
                    omodel = "model=Sat"
            
            elif "_A345" in osim or "_a345" in osim:
                if "Normal" in omodel or "normal" in omodel or "NORMAL" in omodel:
                    new_dst = dst_ai + "TFS_A340-500/"
                    omodel = "model=Normal"
                elif "GE" in omodel or "ge" in omodel :
                    new_dst = dst_ai + "TFS_A340-500/"
                    omodel = "model=Sat"
            
            elif "_A346" in osim or "_a346" in osim:
                new_dst = dst_ai + "TFS_A340-600/"
                omodel = "model=P3D4"
                #omodel = "model=FSX"
            
            elif "_A380" in osim or "_a380" in osim:
                if "EA" in omodel or "ea" in omodel or "Ea" in omodel:
                    new_dst = dst_ai + "TFS_A380_FSX/"
                    omodel = "model=EA"
                elif "RR" in omodel or "rr" in omodel :
                    new_dst = dst_ai + "TFS_A380_FSX/"
                    omodel = "model=RR"    
            
            elif "_B772" in osim or "_b772" in osim:
                if "RR" in omodel or "rr" in omodel:
                    new_dst = dst_ai + "TFS_B777-200/"
                    omodel = "model=rr"
                elif "GE" in omodel or "ge" in omodel :
                    new_dst = dst_ai + "TFS_B777-200/"
                    omodel = "model=ge"
                elif "PW" in omodel or "pw" in omodel:
                    new_dst = dst_ai + "TFS_B777-200/"
                    omodel = "model=pw"
            
            elif "_B77L" in osim or "_b77l" in osim:
                new_dst = dst_ai + "TFS_B777-200LR/"
                omodel = "model="
            
            elif "_B773" in osim or "_b773" in osim:
                if "RR" in omodel or "rr" in omodel:
                    new_dst = dst_ai + "TFS_B777-300/"
                    omodel = "model=rr"
                elif "PW" in omodel or "pw" in omodel :
                    new_dst = dst_ai + "TFS_B777-300/"
                    omodel = "model=pw"
            
            elif "_B77W" in osim or "_b77w" in osim:
                new_dst = dst_ai + "TFS_B777-300ER/"
                omodel = "model="
                
            elif "8-Q100" in osim or "8-q100" in osim:
                if "NL" in omodel or "nl" in omodel  or "Nl" in omodel:
                    new_dst = dst_ai + "TFS_Dash 8-100_200/"
                    omodel = "model=NL"
                else: 
                    new_dst = dst_ai + "TFS_Dash 8-100_200/"
                    omodel = "model="    
            
            elif "8-Q300" in osim or "8-q300" in osim:
                if "NL" in omodel or "nl" in omodel  or "Nl" in omodel:
                    new_dst = dst_ai + "TFS_Dash 8-300/"
                    omodel = "model=NL"
                else: 
                    new_dst = dst_ai + "TFS_Dash 8-300/"
                    omodel = "model="
                    
            elif "8-400" in osim or "8-400" in osim:
                new_dst = dst_ai + "TFS_Dash 8-400/"
                omodel = "model="
                
            elif "AB_340" in osim or "ab_340" in osim:
                new_dst = dst_ai + "TFS_SAAB 340/"
                omodel = "model="
                
            elif "AB_2000" in osim or "ab_2000" in osim:
                new_dst = dst_ai + "TFS_SAAB_2000/"
                omodel = "model=" 
                
# UTT
                
            elif "_B-748" in osim or "_b-748" in osim:
                if "f" in omodel or "F" in omodel:
                    new_dst = dst_ai + "UTT_AI_B748/"
                    omodel = "model=f"
                else:
                    new_dst = dst_ai + "UTT_AI_B748/"
                    omodel = "model="
            
            elif "_B788" in osim or "_b788" in osim:
                new_dst = dst_ai + "UTT_AI_B787-800/"
                omodel = "model="
            
            elif "_B789" in osim or "_b789" in osim:
                new_dst = dst_ai + "UTT_AI_B787-900/"
                omodel = "model="
                
            elif "_CRJ900" in osim or "_Crj900" in osim or "_crj900" in osim:
                new_dst = dst_ai + "UTT_AI_CRJ-900/"
                omodel = "model="
            
            elif "_CRJ1000" in osim or "_Crj1000" in osim or "_crj1000" in osim:
                new_dst = dst_ai + "UTT_AI_CRJ-1000/"
                omodel = "model="
                
            elif "_MD11" in osim or "_Md11" in osim or "_md11" in osim:
                if "GE" in omodel or "ge" in omodel:
                    new_dst = dst_ai + "UTT_AI_MD11/"
                    omodel = "model=GE"
                else:
                    new_dst = dst_ai + "UTT_AI_MD11/"
                    omodel = "model=PW" 
                    
            elif "_SSJ100" in osim or "_Ssj100" in osim or "_ssj100" in osim:
                new_dst = dst_ai + "UTT_AI_SSJ-100/"
                omodel = "model=" 
            
            else:
                print(cfg_lines[posi[k]+1] + ": Can't find model/paint/air/folder.. NOT INSTALLED...")
                h.write(zippath + items[i] + "\n")
                break
            
            tex_name = ("texture." + otexture[8:-1])
            
            
            if os.path.exists(new_dst + "airplane.txt") == False:
                
                if os.path.exists(zip_dir + tex_name) == True:
                    copy_tree((zip_dir + tex_name), (new_dst + tex_name))
                        
                    makecfg = MakeCFG(zip_dir,new_dst,otitle,osim,omodel,otexture,oatc,oatcid,omanu,ouitype,ouivar,odesc,o_code,o_type)   
                    makecfg.writecfg()
                    
                    if "SAAB" in new_dst or "Fokker_50" in new_dst or "OSP" in new_dst or "Dash" in new_dst or "EMB12" in new_dst:
                            speed = '300'
                    elif "71" in new_dst or "727" in new_dst or "MD_8" in new_dst or "DC_9" in new_dst:
                        speed = '430'
                    elif "EMB17" in new_dst or "EMB19" in new_dst or "CRJ" in new_dst or "Fokker_100" in new_dst:
                        speed = '420'
                    elif "73" in new_dst or "318" in new_dst or "319" in new_dst or "320" in new_dst or "321" in new_dst or "SSJ" in new_dst:
                        speed = '450'
                    elif "75" in new_dst or 'A300' in new_dst or 'A310' in new_dst:
                        speed = '460'
                    elif '76' in new_dst or '332' in new_dst or '333' in new_dst:
                        speed = '470'
                    elif '77' in new_dst or 'MD11' in new_dst or 'DC10' in new_dst:
                            speed = '480'
                    elif '74' in new_dst or 'A340' in new_dst or 'A380' in new_dst  or '78' in new_dst or '350' in new_dst:
                            speed = '490'
                
                    print(new_dst + "/" + tex_name + " installed ok!" + "\n")
                    g.write(',' + speed + ',"' + otitle[6:-1] + '"' "\n")
                         
                    
                else:
                    print(new_dst + "/" + tex_name + " ZIP TEXTURE DOESNT MATCH WHATS IN CFG FILE!" + "\n")
                    h.write(zippath + items[i] + "\n")
            
            else:
                d = open(new_dst + "airplane.txt")
                all_entries = [line for line in d if line.strip()]
                entry_str= " ".join(str(x) for x in all_entries)
                d.close()
                if otitle in entry_str:
                    print(new_dst + tex_name + " ALREADY EXISTS, NOT COPIED")
                    
                else:
                    if os.path.exists(zip_dir + tex_name) == True:
                        copy_tree((zip_dir + tex_name), (new_dst + tex_name))
                        
                        makecfg = MakeCFG(zip_dir,new_dst,otitle,osim,omodel,otexture,oatc,oatcid,omanu,ouitype,ouivar,odesc,o_code,o_type)   
                        makecfg.writecfg()
                          
                        if "SAAB" in new_dst or "Fokker_50" in new_dst or "OSP" in new_dst or "Dash" in new_dst or "EMB12" in new_dst:
                            speed = '300'
                        elif "71" in new_dst or "727" in new_dst or "MD_8" in new_dst or "DC_9" in new_dst:
                            speed = '430'
                        elif "EMB17" in new_dst or "EMB19" in new_dst or "CRJ" in new_dst or "Fokker_100" in new_dst:
                            speed = '420'
                        elif "73" in new_dst or "318" in new_dst or "319" in new_dst or "320" in new_dst or "321" in new_dst or "SSJ" in new_dst:
                            speed = '450'
                        elif "75" in new_dst or 'A300' in new_dst or 'A310' in new_dst:
                            speed = '460'
                        elif '76' in new_dst or 'A330-200' in new_dst or 'A330-300' in new_dst:
                            speed = '470'
                        elif '77' in new_dst or 'MD11' in new_dst or 'DC10' in new_dst:
                            speed = '480'
                        elif '74' in new_dst or 'A340' in new_dst or 'A380' in new_dst  or '78' in new_dst or '350' in new_dst:
                            speed = '490'
                            
                        print(new_dst + "/" + tex_name + " installed ok!" + "\n")
                        g.write(',' + speed + ',"' + otitle[6:-1] + '"' "\n")
                        
                        
                    else:
                        print(new_dst + "/" + tex_name + " ZIP TEXTURE DOESNT MATCH WHATS IN CFG FILE!" + "\n")
                        h.write(zippath + items[i] + "\n")
            
        else:
            print(cfg_lines[posi[k]+1] + " NOT INSTALLED...")
            h.write(zippath + items[i] + "\n")
                

g.close()
h.close()
