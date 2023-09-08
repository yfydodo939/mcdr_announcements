# mcdr_announcements
A plugin running on MCDR to send announcements regularly.
<br/>
Run `pip install pyyaml` in cmd or powershell before loading this plugin.

### v1.1.0 update

+ Now commands are allowed to configure instead of editing the yaml file. 

  `!!an`:  Show this help message list

  `!!an enable`:  Enable the timed announcement

  `!!an disable`:  Disable the timed announcement

  `!!an set <message>`:  Set the content of announcement

  <strong>Notice:</strong> `\n` for next line and `&` for the color text. If you use Chinese in this command, please add `-Dfile.encoding=UTF-8` in your start command. Such as `java -Dfile.encoding=UTF-8 -jar server.jar nogui`
  
  `!!an time <seconds>`:  Set the interval time (seconds/time)

+ The status is set to False by default now. Please enable it manually.
+ Only admin and owner can run commands.
