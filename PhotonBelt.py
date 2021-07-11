import PySimpleGUI as sg
import os ,shutil,sys,ctypes

source='C:\Windows\System32\drivers\etc\hosts'
destination='C:\Windows\System32\drivers\etc\hosts.bak'

is_admin=ctypes.windll.shell32.IsUserAnAdmin() #checks if the program is running as admin

if is_admin == 0 :
    
    ctypes.windll.shell32.ShellExecuteW(None, 'runas',sys.executable,''.join(sys.argv),None,1) #reruns the program with admin previliges
    sys.exit() #closes the original running program
    
else:
    
    None

def backup_original_hosts_file():
    if os.path.exists(destination) == True: #checks if a backup exists
        os.remove(destination) #deletes the old backup

    try:
        
        shutil.copyfile(source, destination) #makes a bakcup from hosts file
        sg.Popup("Backup successfull.")
     
    except:
        
        sg.Popup("error accessing file make sure that the app is running as administator")    

def restore_backup_hosts():
    try:
        shutil.copyfile(destination,source)
        sg.Popup('Backup has been restored successfully')
    except:
        sg.Popup('Program has failed to make backup')
        
def add_website():
    if values[0]=='':
        sg.Popup('make sure you entered the name of the website')
    else:
        backup_original_hosts_file()
        try:
            hosts=open(source,'a')
            hosts.write('0.0.0.0 '+ values[0])
            hosts.close()
            sg.Popup('The website has been added successfully!')
        except:
            sg.Popup('Error adding website to blocklist')
def remove_all_websites():
    try:
        with open(source,'r+') as hosts_file:
            hosts_file.truncate(824)
            sg.Popup('websites has been removed successfully')
    except:
        sg.Popup('error removing websites from the list')
    
    
sg.theme('Default1')
layout = [  [sg.Text('press backup to make a backup of the current configration \npress restore to recover the last version of the configration \npress add to add the website to blocklist \nbut make sure that you enter like in this \nexample: spotify.com \npress clear all blocked websites to remove all websites from blocklist')],
            [sg.Text('Enter the website you want to block: '), sg.InputText()],
            [sg.Button('Backup'),sg.Button('Restore'),sg.Button('Add'),sg.Button('Clear all blocked websites')]]

window = sg.Window('PhotonBelt Website Blocker', layout)

while True:
    event, values = window.read()
    
    if event== sg.WINDOW_CLOSED:
        sys.exit()
        
    elif event== 'Backup':
        backup_original_hosts_file()
    
    elif event == 'Restore':
        restore_backup_hosts()
    
    elif event == 'Add':
        add_website()
    elif event == 'Clear all blocked websites':
        remove_all_websites()