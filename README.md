A simple python sorter that attempts to sort your video series and movies into their individual folders. It uses the use of a rule book and config file to do so.

## Configs

Your configuration files are located in $HOME/.config/7m_video_sorter and should contain 2 files, config.yaml and rule_book.conf

### config.yaml
It currently only supports 4 configurations:
1. input_dir
   This is the directory the sorter will scan to locate all the video files you need to sort
2. series_dirs
   This is a list of all the directories where your sorted series are located, the sorter will go through all the folders and subfolders in these directories
3. ignore
   The files that the sorter will ignore in the input directory
4. before_scripts
   A list of scripts you need to run before the sorter runs, great place to put your mount scripts if you need to mount a network drive to sort your videos

### rule_book.conf
This is the rule book the sorter will use to sort your videos. it currently only has 5 available options
1. season
   Sorts the file into its Season ## folder
2. episode-only
   Changes season 1 episode 16 to episode 116, as the matcher sometimes can't tell if its a series without seasons and only episodes. Mainly used for anime
3. parent-dir
   Sets the transfer to the parent directory, doesn't attempt to located the subdirectory this episode should go into. Mainly used for anime
4. subdir-only subdir1
   Sets the transfer to a specific subdirectory only. (use ':' in place of spaces)
5. alt-title :-:
   Sometimes the matcher separates the title into a title and alternative title, if you need them combined, use this option (use ':' in place of spaces)
