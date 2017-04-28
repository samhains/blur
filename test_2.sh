mv ~/Code/pix2pix/results/nolikes256/latest_net_G_val/images/output ~/Code/pix2pix/results/nolikes256/latest_net_G_val/images/output_old &&
	mv ~/Code/pix2pix/results/nolikes256/latest_net_G_val/images/input ~/Code/pix2pix/results/nolikes256/latest_net_G_val/images/input_old 
	mv ~/Code/pix2pix/data/val ~/Code/pix2pix/data/val_old &&
	mkdir ~/Code/pix2pix/data/val_2 &&
	python ~/Code/pix2pix/data/get_missing_files.py
	mv ~/Code/pix2pix/data/val_2 ~/Code/pix2pix/data/val
	./test.sh &&
	mv ~/Code/pix2pix/results/nolikes256/latest_net_G_val/images/input/* ~/Code/pix2pix/results/nolikes256/latest_net_G_val/images/input_old &&
	mv ~/Code/pix2pix/results/nolikes256/latest_net_G_val/images/output/* ~/Code/pix2pix/results/nolikes256/latest_net_G_val/images/output_old &&
	rm -r ~/Code/pix2pix/results/nolikes256/latest_net_G_val/images/input &&
	rm -r ~/Code/pix2pix/results/nolikes256/latest_net_G_val/images/output &&
	mv ~/Code/pix2pix/results/nolikes256/latest_net_G_val/images/input_old ~/Code/pix2pix/results/nolikes256/latest_net_G_val/images/input &&
	mv ~/Code/pix2pix/results/nolikes256/latest_net_G_val/images/output_old ~/Code/pix2pix/results/nolikes256/latest_net_G_val/images/output



