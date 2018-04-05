A simple python sorter that attempts to sort your video series and movies into their individual folders. It uses the use of a rule book and config file to do so.

## Installation

```bash
git pull https://github.com/Scheercuzy/mxs_video_sorter.git
cd mxs_video_sorter
virtualenv -p python3 env
source env/bin/activate
pip install .
```

## Usage

The first time you run it, it will complain about not being able to find your input_dir, you will have to head to the [configs](#configs) and configure your config.yaml with your input_dir and series_dirs.
Once done, run it again to start.
```bash
python mxs_video_sorter/main.py
```
You will see the result of the search but nothing will be transfered, and probably a bunch of "NOT IN LIST" or "NO MATCH"

### Learn by Example
This is the structure of the `myseries/` we will use
```
myseries/ <--- "Location of your output_dirs in your config.yaml file"
├── Blue\ Mountain\ State
│   ├── Season\ 1
│   ├── Season\ 2
│   └── Season\ 3
├── Homeland
│   └── All Episodes
├── House\ MD
├── Lucifer
│   ├── Season\ 1
│   ├── Season\ 2
│   └── Season\ 3
...
```
These are the files and folders in my `downloads/` folder
```
downloads/ <--- "Location of your input_dir in your config.yaml file"
├── Lucifer.S01E15
│   ├── Lucifer.S01E15.mkv
│   └── ...
├── House\ MD.S09E12.mkv
├── Homeland.S05E14.mkv
```
We will first start by adding both our folders to our config, Therefore head to your `config.yaml` in `$HOME/.config/mxs_video_sorter/config.yaml` and add these folders:
```
input_dir: "absolute/path/to/downloads"

series_dirs:
  - "absolute/path/to/myseries"
```
- Note that the series folder is a list and the input_dir is a value, this is because right now the program does not support multiple input directories

In my `series/` file, there are 3 types of arrangements:
1. Blue Mountain State and Lucifer has a subdirectory for each season of the show
2. Homeland has a subdirectory for all its video files
3. House MD places it directly into the parent directory

These are all rules that we need specify in the rule_book for the program to know which is which. Therefore head to your `rule_book.conf` in `$HOME/.config/mxs_video_sorter/rule_book.conf` and make these rules:
```
[series_rules]
Blue Mountain State=season
Lucifer=season
Homeland=subdir-only "All Episodes"
House MD=parent-dir
```
You should now see each show title with the INFO "MATCHED" below it, but it will not transfer the files yet.

When running the program will always show INFO on each files with either a "MATCHED", "NO MATCH", or "NOT IN LIST". "NO MATCH" means it couldn't match the video file to the series folder, "NOT IN LIST" means it couldn't find the video file title on the rule_book and "MATCHED" means good news :)

before transfering your video files to their corresponding directory, add the argument `-r` (--review) to have a more detailed review of all the matches and where they will end up to be sure. This will show you 1 by 1 where the files will end up and more detailed information on the matching of your files

When you are satisfied with your review, its time to do the actual transfering. This time run the program with the argument `-t` (--transfer) to have all the files moved to their new folders and deleted from their source. if you wish to keep the files in the source, pass the `-p` (--prevent-delete) and your files will stay intact.

## Configs

Your configuration files are located in $HOME/.config/mxs_video_sorter and should contain 2 files, config.yaml and rule_book.conf

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
4. subdir-only "subdir name"

   Sets the transfer to a specific subdirectory only.
5. alt-title " - "

   Sometimes the matcher separates the title into a title and alternative title, if you need them combined, use this option
