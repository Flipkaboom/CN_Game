from Entities import entity, animation

class LargePlatform(entity.Entity):
    idle_anim = animation.Animation('playing_large_platform')

class SmallPlatform(entity.Entity):
    idle_anim = animation.Animation('playing_small_platform')
