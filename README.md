# Particle-Attraction
A small application that allows the user to place particles that interact with each other. 

## Description
I originally made this program because I thought it would look cool to visualize the movement of particles when they start interacting with each other.

To start, we must create a 'blueprint' for the particles.

```py
  def __init__(self, x, y, vx, vy, mass, radius):
    self.x = x # x position
    self.y = y # y position
    self.vx = vx # x velocity
    self.vy = vy # y velocity
    self.mass = mass
    self.radius = radius
```

Now we have the outline of our particle, the next step is to figure out the new x and y positions when it is moving.
To do this we can use the following velocity equation:

<p align="center">$\text{v} = \frac{\Delta\text{s}}{\Delta\text{t}}$</p>

From this equation, we can rearrange for displacement and add it to our x and y values.

<p align="center">Δs = v ⋅ Δt</p>

```py
  def UpdatePosition(self, dt):
    self.x += self.vx * dt
    self.y += self.vy * dt
```


We can now do the fun part... Calculating the Gravitational Force!!

For this, we are going to use Newton's Law of Universal Gravitation:

<p align="center">F = G ⋅ m1⋅m2/r^2</p>
