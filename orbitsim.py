import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

G = 6.6743 * 10 ** -11
Mm = 7.34767 * 10 ** 22
Me = 5.97219 * 10 ** 24
Ms = 1.9891 * 10 ** 24
Rs = 1.49597 * 10 ** 9
Re = 3.844 * 10 ** 8
Ve = 29782.7 / 100
Vm = 1022.0

class Star:
    def __init__(self, mass, position: np.array):
      self.mass = mass
      self.position = position

class Planet:
    def __init__(self, mass, position: np.array, velocity: np.array, acceleration: np.array, parent = None):
      self.mass = mass
      self.position = position
      self.velocity = velocity
      self.acceleration = acceleration
      self.parent = parent

    def get_accel(self):
      if self.parent:
        r = self.position - self.parent.position
        d = np.linalg.norm(self.position - self.parent.position)
        rhat = r / d
        self.acceleration = -G * (self.parent.mass / (d ** 2)) * rhat

    def move(self, delta_t):
      self.position += self.velocity * delta_t
      self.get_accel()
      self.velocity += self.acceleration * delta_t  

class PlanetSystem:
    def __init__(self, position: np.array, primary: Planet, secondary: Planet, dt: int):
      self.position = position
      self.primary = primary
      self.secondary = secondary
      self.dt = dt

    def step(self):
      p = self.primary
      m = self.secondary
      m.move(self.dt)
      current_pos = np.copy(p.position)
      p.move(self.dt)
      new_pos = p.position
      m.position += (new_pos - current_pos)
      return {'x': [p.position[0], m.position[0], 0], 'y': [p.position[1], m.position[1], 0], 'z': [p.position[2], m.position[2], 0]}


def create_gif(model: PlanetSystem, steps_per_frame, frames, filename):
  
  fig = plt.figure(figsize=(15,15), facecolor='black')
  ax = fig.add_subplot(projection='3d')
  scatter = ax.scatter3D([0], [0], [0], sizes=[30, 10, 500])

  ax.set_xlim(-2.0e9, 2.0e9)
  ax.set_ylim(-2.0e9, 2.0e9)
  ax.set_zlim(-2.0e9, 2.0e9)
  ax.view_init(elev=90)
  ax.set_facecolor('black')
  ax.set_axis_off()

  def init():
    scatter._offsets3d = ([0], [0], [0])
    return scatter,

  def animate(i):
    for j in range(steps_per_frame):
      model.step()
    data = model.step()
    scatter._offsets3d = (data['x'], data['y'], data['z'])
    scatter.set_color(['blue', 'white', 'yellow'])
    return scatter,


  anim = animation.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=50, blit=True)
  anim.save(f'{filename}.gif', writer='pillow', fps=20)

sun = Planet(Ms, np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([0, 0, 0]))
earth = Planet(mass=Me, position=np.array([0, Rs, 0]), velocity=np.array([Ve, 0, 0]), acceleration=np.array([0, 0, 0]), parent=sun)
moon = Planet(Mm, np.array([0, Re + Rs, 0]), np.array([Vm*0.996, 0, Vm*0.0889]), np.array([0, 0, 0]), earth)
system = PlanetSystem(np.array([0, 0, 0]), earth, moon, 500)

create_gif(system, 100, 400, 'test19')