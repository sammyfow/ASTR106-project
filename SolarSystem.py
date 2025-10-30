import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

G = 6.6743 * 10 ** -11
Me = 5.97219 * 10 ** 24
Ms = 1.9891 * 10 ** 30
R = 1.49597 * 10 ** 11
v = 29782.7

class Planet:
    def __init__(self, mass, position: np.array, velocity: np.array, acceleration: np.array):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

class SolarSystem:
    def __init__(self, planet: Planet, dt: int):
        self.planet = planet
        self.dt = dt

    def get_accel(self):
        r = self.planet.position
        d = np.linalg.norm(self.planet.position)
        rhat = r / d
        accel = -G * (Ms / (d ** 2)) * rhat
        return accel

    def step(self):
        self.planet.position += self.planet.velocity * self.dt
        self.planet.acceleration = self.get_accel()
        self.planet.velocity += self.planet.acceleration * self.dt
        return {'x': self.planet.position[0], 'y': self.planet.position[1], 'z': self.planet.position[2]}



def create_gif(model: SolarSystem, steps_per_frame, frames, filename):
  
  fig = plt.figure()
  ax = fig.add_subplot(projection='3d')
  scatter = ax.scatter3D([0], [0], [0])

  ax.set_xlim(-2e11, 2e11)
  ax.set_ylim(-2e11, 2e11)
  ax.set_zlim(-2e11, 2e11)
  ax.set_xlabel("X (m)")
  ax.set_ylabel("Y (m)")
  ax.set_zlabel("Z (m)")
  ax.set_title("Planet Orbit")
  ax.view_init(elev=90)

  def init():
    scatter._offsets3d = ([0], [0], [0])
    return scatter,

  def animate(i):
    for j in range(steps_per_frame):
      model.step()
    data = model.step()
    scatter._offsets3d = ([0, data['x']], [0, data['y']], [0, data['z']])
    return scatter,


  anim = animation.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=50, blit=True)
  anim.save(f'{filename}.gif', writer='pillow', fps=20)

earth = Planet(Me, np.array([0, R, 0]), np.array([v, 0, 0]), np.array([0, 0, 0]))
system = SolarSystem(earth, 1000)
create_gif(system, 100, 300, 'test1')