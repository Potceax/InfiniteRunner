# InfiniteRunner package

This is a package containing the replica of a chrome dino game. You can play it by downloading it from
[here](https://github.com/Potceax/InfiniteRunner) with command: 

```bash
py -m pip install "git+https://github.com/Potceax/InfiniteRunner.git#egg=Game_Karol_Warda"
```

# How to run

To run this game you need to:

1. Download the package
2. Move assets to destination described in Assets section
3. In new .py file type:
  ```python
  from Game_Karol_Warda import Game

  if __name__ == "__main__":
    Game.play()
  ```
4. Run the .py script

# Assets

Required assets and documentation can be downloaded from the [main repo](https://github.com/Potceax/InfiniteRunner). 
Assets (Images folder and .ttf) should be placed into the pip library folder of the project: 

```plaintext
path-to-python\lib\site-packages\Game_Karol_Warda\
```

NOTE the Images folder and .ttf should be separated from assets folder before moving them to pip library folder
