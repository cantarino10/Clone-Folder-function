import os,time,sys
from shutil import copy2     
from datetime import datetime,timedelta
from filecmp import cmp

def creat_folder(log_path,path): #function to create folder and register at logfile
  try:
      os.makedirs(path) #Try to create a new folder
      
  except:
       print("Invalid Path destination path. Try again\n") #Return if the path is valid
       return False
  else:
    print(f"{path} Was created")  
     
    with open(f"{log_path}\\logfile.txt", "a") as log: #Register folder creation at logfile
        log.write(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {path} was created\n")
        log.close()
        return True 


def main(source_folder,destination_folder,synchronization_interval : int,log_path): #main
 try:
   synchronization_interval = int(synchronization_interval) #check if interval is valid
 except:
   print("Invalid value for time interval")  
   return

 if not os.path.exists(log_path):
   get_input = input("The path for logfile folder does not exist type Y to create a new one ?")
   if get_input == "y" or get_input == "Y":   #Create a new logfile path 
     if not creat_folder(log_path,log_path):
       return

 if not os.path.exists(source_folder):   # Check if the source path exist
  get_input = input("The path for  source folder does not exist type Y to create a new one ?")
  if get_input == "y" or get_input == "Y":   #Create a new logfile path 
     if not creat_folder(log_path,source_folder):
       return
 
 if len(os.listdir(source_folder)) == 0:   # Check if the source path have files
   print("###WARNING### this folder is empty\n")
   time.sleep(3)       # Give a break so the user will be able to se the message
 
 if source_folder == destination_folder:
   print("New folder path is the same as source folder. Please try with another one \n")   # Check if both folder are the same
   return

 elif not os.path.exists(destination_folder):# Check if destination folder exist 
   if not os.path.exists(destination_folder): #check if log path does exist
    get_input = input("The path for destination folder does not exist type Y to create a new one ?")
    if get_input == "y" or get_input == "Y":
      if not creat_folder(log_path,destination_folder): #try to create folder for destination
        return

  
 backuptime = datetime.now()  #Time of doing bacup
 errors = False
 while True:
  
  if backuptime <= datetime.now() : #check if destination or logfile folder wasnt deleted by acident (it already happened with me)
   
   if not os.path.exists(log_path): 
     if not creat_folder(log_path,log_path):
       return
   if not os.path.exists(destination_folder): 
     if not creat_folder(log_path,destination_folder):  
        return
     
   with open(f"{log_path}/logfile.txt", "a") as log: # open log folder
    for files in os.listdir(destination_folder):
     file =  destination_folder + "/" + files   #got path of files

     if not files in os.listdir(source_folder): #check if there is the same file at origin past, and delete if it\s not
       try: 
         os.remove(destination_folder + "\\" +files)    #clean the folder to receive new files 
       except:
          errors = True
          remove_text = f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ###WARNING### {file} could have not been removed" #tell if file wasnt remove
       else:
         remove_text = f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {file} have been sucessfully removed"  #tell if it was
    
       print(remove_text)              #print on the console and logfile    
       log.write(f"remove_text \n")
  
    if len(os.listdir(source_folder)) == 0:
     text = print("The source directory is empty there is no files to copy") #check if stil have files in source directory
     errors = False
    else :      
     for file in os.listdir(source_folder):
      try:
        overwrite = not cmp((source_folder + "\\" + file),(destination_folder + "\\" + file))  #check if this file already exist and if it does, check if it is unchagend to avoid more process would be useful to avoide wast of time on larger files
    
      except:
        overwrite = True      #if dont exist or de program cant compare for any reason will overwrite it

      if overwrite == True:   #if this file does not exist, or was modified than copy to the clone folder
        try: 
          copy2(source_folder + "\\" + file,destination_folder+"\\"+file) #copy function
        except:
             errors = True
             text = (f"#####WARNING Could not copy ({file})") #Warning in case of cant copy for any reason
            
        else:   
             text = (f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {file} Has been cloned to : {destination_folder}" )  #Notify if the file was copied
      else:
       text = (f"This file {file} does not have any modification")      #notify if ti does not have modifications
      print(text)
      log.write(f"{text} \n")
    log.close
    backuptime = datetime.now() + timedelta(seconds=synchronization_interval) #update counter
    if errors == False:
        print(f"All files Have been sucessfully cloned. Logfile at {log_path}\\logfile.txt.")
    else:                                                                                       
         print(f"Process has finished with some erros check. Logifle at  {log_path}\\logfile.txt.") #Tell if it has any errors
    print(f"\nNext copy at {backuptime.strftime("%Y-%m-%d %H:%M:%S")}\n. Press Ctrl + C to stop")         
      
  try:
    time.sleep(5) #Shorter time between copies to: be able to visuzalize informations, avoid bottlenecks and can stop the program with keyboard interrupt 
  except:
    print("Program finished")
    return #if any key be pressed on sleep time
 
if __name__ == "__main__":
  if len(sys.argv) == 5:
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
  else:
    print("Unsuficient arguments -> (source_folder, destination_folder, synchronization_interval : int, log_path)") 
