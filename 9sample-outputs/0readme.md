- [scales-full.musicxml](scales-full.musicxml)  
  output from ../solfege192_demo.py scales --length=full
- [shearer-c.txt](shearer-c.txt)  
  output from ../solfege192_demo.py textart
- [shearer-cs.txt](shearer-cs.txt)  
  output from ../solfege192_demo.py textart --key=Cs
- [movable-do-cs.txt](movable-do-cs.txt)  
  output from ../solfege192_demo.py --movable-do textart --key=Cs
- [shearer-cf-de.txt](shearer-cf-de.txt)  
  output from ../solfege192_demo.py textart --key=Cf de
- [movable-do-cf-de.txt](movable-do-cf-de.txt)  
  output from ../solfege192_demo.py --movable-do textart --key=Cf de
- [scales-half-sinsy.mp3](scales-half-sinsy.mp3)  
  $ ../solfege192_demo.py scales --length=half > scales-half.musicxml  
  $ ../cheatweb-sinsy scales-half.musicxml  
  $ ffmpeg -i scales-half-sinsy.wav scales-half-sinsy.mp3
