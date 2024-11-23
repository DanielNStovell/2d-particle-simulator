import pygame
import random

pygame.init()

width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Particle")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# A class to act as a blue print for our particles
class PARTICLE(object):
  """
  x : The x position of the particle
  y : The y position of the particle
  vx : The x velocity of the particle in ms^-1
  vy : The y velocity of the particle in ms^-1
  mass : The mass of the particle in kg
  radius : The radius of the particle in m
  """
  def __init__(self, x, y, vx, vy, mass, radius, ifx=0, ify=0):

    # Applying our needed variables for each particle
    self.x = x
    self.y = y
    self.vx = vx
    self.vy = vy
    self.mass = mass
    self.radius = radius

    self.ifx = ifx
    self.ify = ify

    """
    self.lastPositionCount = 100
    self.lastPositionPointer = 0
    self.lastPositions = ["."]*self.lastPositionCount
    """
    self.forceApplied = False  

  """
  To aquire the new position of the particle we can just use the velocity equation: v = s/t
  We can rearrange this equation for displacement: s = v * t
  Now we can add this displacement to the original position of the particle to get our new position
  """

  def UpdatePosition(self, dt):

    """
    self.lastPositions[self.lastPositionPointer % self.lastPositionCount] = [self.x, self.y]
    self.lastPositionPointer += 1
    """

    # Updating position by adding displacement
    self.x += self.vx * dt
    self.y += self.vy * dt

  """
  To update the velocity of the particle we need to use Newton's second law of motion: F = ma
  We can rearrange this equation for acceleration (a): a = F/m
  Since acceleration is v/t, we can find the new velocity by multiplying acceleration by time: v_new = a * dt
  """

  def UpdateVelocity(self, dt, other, mouse):

    if not self.forceApplied:
      
      ax = self.ifx / self.mass
      ay = self.ify / self.mass

      self.vx += ax * dt
      self.vy += ay * dt 

      self.forceApplied = True

    XFORCES = []
    YFORCES = []

    # gravity of other particles
    ox, oy, om = other.x, other.y, other.mass

    if mouse:
      ox, oy = pygame.mouse.get_pos()
      om = 10

    r = ((self.x - ox)**2 + (self.y - oy)**2)**0.5
    if r == 0:
      r = 1e-1
    G = 10
    epsilon = 3
    F = G * (self.mass * om) / (r**2 + epsilon**2)
    F_x = F * ((ox - self.x)/r)
    F_y = F * ((oy - self.y)/r)
    XFORCES.append(F_x)
    YFORCES.append(F_y)

    # Air drag
    dragCoefficient = 0.01
    F_dragx = -dragCoefficient * self.vx
    F_dragy = -dragCoefficient * self.vy
    #XFORCES.append(F_dragx)
    #YFORCES.append(F_dragy)

    F_totalx = sum(XFORCES)
    F_totaly = sum(YFORCES)

    ax = F_totalx/self.mass
    ay = F_totaly/self.mass

    # Adding calculated velocities to the original
    self.vx += ax * dt
    self.vy += ay * dt 

  """
  We want to check if the particle has collided with a wall
  To do this we can get the position of the particles and check if they are out of the boundries (collided with a wall)
  We will assume that we have a perfectly elastic wall (there is no loss in the velocity due to friction)
  To achieve this bouce we can just invert the velocity that is perpendicular to the wall

      For a verticle wall (e.g. x = 0) the x velocity will be inverted: (vx', vy') = (-vx, vy)

      For a horizontal wall (e.g. y = 0) the y velocity will be inverted: (vx', vy') = (vx, -vy)
  """

  def CheckBoundary(self, xr, xl, yu, yd):

    # Checking if the borders are not valid (xl > xr & yd > yu)
    if xl > xr or yd > yu:
      return "Not valid boundaries"

    # Cheking if the positions of the particle go past the borders
    if self.x > xr or self.x < xl:
      self.vx = -self.vx 
    if self.y > yu or self.y < yd:
      self.vy = -self.vy 

  """
  def GetLastPositions(self):
    return self.lastPositions
  """

  def GetData(self):
    
    # Returning data about the particle for debugging
    return f"Particle is at ({self.x},{self.y}) moving with a velocity of ({self.vx},{self.vy})"

def UpdateParticle(particle, dt, fx, fy, other, mouse=False):

  particle.CheckBoundary(width,0,height,0)
  particle.UpdatePosition(dt)
  particle.UpdateVelocity(dt, other, mouse)

particleList = []
num = 1
speed = 500

for i in range(num):
  particleList.append(PARTICLE(random.randint(50, width-50), random.randint(50, height-50), 0, 0, 5, 1))
  #particleList.append(PARTICLE(random.randint(50, width-50), height//2, 0, 0, 1, 1, 0, 0))

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  screen.fill(black)

  for i, particle in enumerate(particleList):
    for j, otherParticle in enumerate(particleList):
      if i != j:
        UpdateParticle(particle, 0.01, 0, 0, otherParticle)
      UpdateParticle(particle, 0.01, 0, 0, otherParticle, True)
    pygame.draw.circle(screen, white, (int(particle.x), int(particle.y)), particle.radius)
    #screen.set_at((int(particle.x), int(particle.y)), white)

    """
    for lastPos in particle.GetLastPositions():
      if lastPos != ".":
        screen.set_at((int(lastPos[0]),int(lastPos[1])), white)
    """

  pygame.display.flip()

pygame.quit()
