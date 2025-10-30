import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

G = 6.6743 * 10 ** -11
Mm = 7.34767 * 10 ** 22
Me = 5.97219 * 10 ** 24
Ms = 1.9891 * 10 ** 30
Rs = 1.49597 * 10 ** 11
Re = 3.844 * 10 ** 8
Ve = 29782.7
Vm = 1022

class Star:
    def __init__(self, mass, position: np.array):
      self.mass = mass
      self.position = position

class Planet:
    def __init__(self, parents, mass, position: np.array, velocity: np.array, acceleration: np.array):
      self.parents = parents
      self.mass = mass
      self.position = position
      self.velocity = velocity
      self.acceleration = acceleration

class SolarSystem:
    def __init__(self, star: Star, planets: list, dt: int):
      self.star = star
      self.planets = planets
      self.dt = dt

    def get_accel(self, planet: Planet):
      accel = 0
      for p in planet.parents: 
        r = planet.position - p.position
        d = np.linalg.norm(planet.position - p.position)
        rhat = r / d
        a = -G * (p.mass / (d ** 2)) * rhat
        accel += a
      return accel

    def step(self):
      for p in self.planets:
        p.position += p.velocity * self.dt
        p.acceleration = self.get_accel(p)
        p.velocity += p.acceleration * self.dt
      return {'x': [p.position[0] for p in self.planets] + [0], 'y': [p.position[1] for p in self.planets] + [0], 'z': [p.position[2] for p in self.planets] + [0]}



def create_gif(model: SolarSystem, steps_per_frame, frames, filename):
  
  fig = plt.figure(figsize=(15,15))
  ax = fig.add_subplot(projection='3d')
  scatter = ax.scatter3D([0], [0], [0], s=0.25)

  ax.set_xlim(0.2e11, 0.6e11)
  ax.set_ylim(1.2e11, 1.6e11)
  ax.set_zlim(1e11, 2e11)
  ax.view_init(elev=90)

  def init():
    scatter._offsets3d = ([0], [0], [0])
    return scatter,

  def animate(i):
    for j in range(steps_per_frame):
      model.step()
    data = model.step()
    scatter._offsets3d = (data['x'], data['y'], data['z'])
    return scatter,


  anim = animation.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=50, blit=True)
  anim.save(f'{filename}.gif', writer='pillow', fps=20)

sun = Star(Ms, np.array([0, 0, 0]))
earth = Planet([sun], Me, np.array([0, Rs, 0]), np.array([Ve, 0, 0]), np.array([0, 0, 0]))
moon = Planet([earth, sun], Mm, np.array([0, Rs + Re, 0]), np.array([Ve + Vm, 0, 0]), np.array([0, 0, 0]))
system = SolarSystem(sun, [earth, moon], 100)

create_gif(system, 100, 300, 'test3')