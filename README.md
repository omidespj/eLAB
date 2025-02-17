1.	Enable Hyper-V:
•	Press Win + R, type optionalfeatures.exe, and press Enter.
•	In the Windows Features dialog, check the box for Hyper-V and click OK.
•	Restart your computer if prompted.

2.	Download ISO file for OS, Ubuntu LTS
3.	Run Hyper V manager as administrator
4.	In the left-hand side panel under Hyper V manager select your local computer
5.	Then in the action panel in the right side click new and then click virtual computer
6.	Afterward click next, then choose a name and if you intend change the directory of VM installation
7.	Click next, choose generation 1 and click next
8.	Assign desired RAM and click next
9.	For the connection choose Default Switch and click next
10.	 Now assign the storage capacity under Create a virtual hard disk
11.	Click next and choose installing OS from image file (2nd option)
12.	If you are not able to browse the iso file, paste the directory in the browse bar manually like C:\Users\YourUsername\Downloads\OS.iso
13.	Then click next and finish.
14.	Then right click on the virtual machine click start and then connect
15.	Do the installation of OS until it finishes
16.	Run the OS and load it
17.	Open the terminal and run these commands: sudo apt update && sudo apt upgrade -y
18.	Run these commands one by one to install and run docker: 
•	sudo install -m 0755 -d /etc/apt/keyrings
•	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc > /dev/null
•	sudo chmod a+r /etc/apt/keyrings/docker.asc
•	echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
•	sudo apt update
•	sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
•	sudo systemctl status docker
19.	If it says active (running) it is fine otherwise you need to start docker manually:
•	sudo systemctl start docker
•	sudo systemctl enable docker
20.	Now we need to install docker compose:
•	sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
•	sudo chmod +x /usr/local/bin/docker-compose
•	docker-compose –version
if it shows the version you are set with that
21.	Now its time to install and set up eLabFTW:
•	mkdir -p ~/elabftw && cd ~/elabftw
•	curl -so docker-compose.yml https://get.elabftw.net/?config
•	curl -o docker-compose.yml https://raw.githubusercontent.com/elabftw/elabimg/master/src/docker-compose.yml-EXAMPLE
•	sudo docker ps
after running it, you should see a list of running docker containers.




