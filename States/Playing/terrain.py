from Entities import entity, animation

class LargePlatform(entity.Entity):
    idle_anim = animation.Animation('playing_large_platform')

class SmallPlatform(entity.Entity):
    idle_anim = animation.Animation('playing_small_platform')

class Clouds(entity.Entity):
    idle_anim = animation.Animation('playing_clouds')

class CloudRight(entity.Entity):
    idle_anim = animation.Animation('cloud_right')

class CloudLeft(entity.Entity):
    idle_anim = animation.Animation('cloud_left')

class CloudUp(entity.Entity):
    idle_anim = animation.Animation('cloud_up')

class CloudDown(entity.Entity):
    idle_anim = animation.Animation('cloud_down')