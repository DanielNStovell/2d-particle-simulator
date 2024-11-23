import pygame
import time

pygame.init()

width, height = 1300, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Particle")

black = (0, 0, 0)
white = (255, 255, 255)

class PARTICLE(object):
  def __init__(self, x, y, vx, vy, mass, radius):
    self.x = x
    self.y = y
    self.vx = vx
    self.vy = vy
    self.mass = mass
    self.radius = radius

  def UpdatePosition(self, dt):
    self.x += self.vx * dt
    self.y += self.vy * dt

  def UpdateVelocity(self, dt, other):

    XFORCES = []
    YFORCES = []

    r = ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
    if r == 0:
      r = 1e-1
    G = 10
    epsilon = 3
    F = G * (self.mass * other.mass) / (r**2 + epsilon**2)
    F_x = F * ((other.x - self.x)/r)
    F_y = F * ((other.y - self.y)/r)
    XFORCES.append(F_x)
    YFORCES.append(F_y)

    """
    # Air drag
    dragCoefficient = 0.01
    F_dragx = -dragCoefficient * self.vx
    F_dragy = -dragCoefficient * self.vy
    XFORCES.append(F_dragx)
    YFORCES.append(F_dragy)
    """

    F_xtotal = sum(XFORCES)
    F_ytotal = sum(YFORCES)

    ax = F_xtotal/self.mass
    ay = F_ytotal/self.mass

    self.vx += ax * dt
    self.vy += ay * dt 

  def CheckBoundary(self, xr, xl, yu, yd):
    if xl > xr or yd > yu:
      return "Not valid boundaries"

    if self.x > xr or self.x < xl:
      self.vx = -self.vx 
    if self.y > yu or self.y < yd:
      self.vy = -self.vy 

  def GetData(self):
    sf = 2
    return f"Particle is at ({round(self.x, sf)}, {round(self.y, sf)}) moving with a velocity of ({round(self.vx, sf)}, {round(self.vy, sf)})"

def UpdateParticle(particle, dt, other):
  particle.CheckBoundary(width,0,height,0)
  particle.UpdatePosition(dt)
  particle.UpdateVelocity(dt, other)

particleList = []
click = False

running = True

dt = 0.01
dtSave = dt
frozen = False

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    if event.type == pygame.MOUSEBUTTONDOWN:
      click = True

    if event.type == pygame.KEYDOWN:
      if not frozen:
        if event.key == pygame.K_q and dt > 0:
          dt -= 0.01
          dtSave = dt
        if event.key == pygame.K_e :
          dt += 0.01
          dtSave = dt
      
      if event.key == pygame.K_w:
        frozen = not frozen

        if frozen:
          dt = 0
        else:
          dt = dtSave

  screen.fill(black)

  font = pygame.font.Font('freesansbold.ttf', 15)

  text = font.render(f"dt: {round(dt,3)}", True, white)
  textRect = text.get_rect()
  textRect.topright = (width, 0)
  screen.blit(text, textRect)

  controls1 = font.render(f"Q&E: Increase/Decrease dt", True, white)
  controls1Rect = controls1.get_rect()
  controls1Rect.bottomleft = (0, height-20)
  screen.blit(controls1, controls1Rect)
  controls2 = font.render(f"W: Pause/Play dt", True, white)
  controls2Rect = controls1.get_rect()
  controls2Rect.bottomleft = (0, height)
  screen.blit(controls2, controls2Rect)

  
  if click:
    click = False
    mx, my = pygame.mouse.get_pos()
    particleList.append(PARTICLE(mx, my, 0, 0, 5, 1))

  for i, particle in enumerate(particleList):
    for j, otherParticle in enumerate(particleList):
      if i != j:
        UpdateParticle(particle, dt, otherParticle)
    pygame.draw.circle(screen, white, (int(particle.x), int(particle.y)), particle.radius)

    
    particleText = font.render(f"{i+1}: {particle.GetData()}", True, white)
    particleTextRect = particleText.get_rect()
    particleTextRect.topleft = (0,0 + 20*i)
    screen.blit(particleText, particleTextRect)

  pygame.display.flip()

pygame.quit()
