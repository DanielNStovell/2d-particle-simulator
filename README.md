# Particle-Attraction
A small program that allows the user to place particles that interact with each other. 

![](https://raw.githubusercontent.com/DanielNStovell/particle-attraction/refs/heads/main/particle%20attraction%20Demo.gif)

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

Now we have the outline of our particle, the next step is to work out the new x and y positions when it is moving.
To do this we can use the following velocity equation:

<p align="center">$\large v = \frac{\Delta s}{\Delta t}$</p>

From this equation, we can rearrange for displacement and add it to our x and y values.

<p align="center">$\large \Delta s_x = v_x \cdot \Delta t$</p>
<p align="center">$\large \Delta s_y = v_y \cdot \Delta t$</p>

```py
  def UpdatePosition(self, dt):
    self.x += self.vx * dt
    self.y += self.vy * dt
```

Now... we can do the fun part... Calculating the Gravitational Force!!

For this, we are going to use Newton's Law of Universal Gravitation:

<p align="center">$\large F= G \frac{m_1 m_2}{r^2}$</p>

We start by finding the distance between the particle and other particles.
To ensure we don't divide by 0, if the distance is 0 we can set it to 1e-3.

```py
    # Pythagorean theorem to find the distance between the particles
    r = ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    # Prevents dividing by 0
    if r == 0:
      r = 1e-3 # 0.001
```

Now we set our constants like the Gravitational constant and epsilon.

I added an epsilon because while I was testing I found my particles started flying everywhere at high speeds so the epsilon is here to prevent that from happening.

```py
    G = 10 # Graviational Constant
    epsilon = 3 # Prevents small devisors
```

COMBINEEE!!

```py
    # Newton's Law of Univeral Gravitation
    F = G * (self.mass * other.mass) / (r**2 + epsilon**2)
```

To put the Gravitational Force into use, we need to apply it to our velocity.
However, we need to separate the Force into x and y components.

```py
    # Using trigonometry to split the force for x and y
    F_x = F * ((other.x - self.x)/r)
    F_y = F * ((other.y - self.y)/r)
```

Using Newton's Second Law of Motion, we can find the acceleration from the forces as we have the particle's mass.

<p align="center">$\large F = ma$</p>
rearranging for acceleration:
<p align="center">$\large a = \frac{F}{m}$</p>

```py
    # Newton's Second Law of Motion
    ax = F_xtotal/self.mass
    ay = F_ytotal/self.mass
```

With the equation for acceleration:

<p align="center">$\large a = \frac{\Delta v}{\Delta t}$</p>

We can rearrange for velocity:

<p align="center">$\large \Delta v_x = a_x \cdot \Delta t$</p>
<p align="center">$\large \Delta v_y = a_y \cdot \Delta t$</p>

We can add them to the original velocities do acquire the new ones

```py
    self.vx += ax * dt
    self.vy += ay * dt
```

That is it for the maths & physics side of the program :)

However, I want to mention how particles reflect off walls as the particle's velocity is affected.

If the particle collides with a verticle wall the x velocity is reversed.
Similarly, if the particle collides with a horizontal wall the y velocity is also reversed.

```py
  def CheckBoundary(self, rightWall, leftWall, topWall, bottomWall):
    # Checks if the arrangement of each walls are correct
    if leftWall > rightWall or bottomWall > topWall:
      return "Not valid boundaries"

    # Colliding with a vertical wall causes the x velocity to reverse
    if self.x > rightWall or self.x < leftWall:
      self.vx = -self.vx 

    # Colliding with a horizontal wall causes the y velocity to reverse
    if self.y > topWall or self.y < bottomWall:
      self.vy = -self.vy 
```
