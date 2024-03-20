

Install:

  #pip install uv
  curl -LsSf https://astral.sh/uv/install.sh | sh

  uv venv
  uv pip install -r requirements.txt

Setup:
  source .venv/bin/activate

# Theory

The one dimentional wave equation can be expressed as the following partial differential equation (PDE):
$$
\frac{\partial^2 u}{\partial t^2} = c^2 \frac{\partial^2 u}{\partial x^2}
$$

Where:
- $u$ is the displacement
- $t$ is time
- $x$ is the spatial coordinate

The numerical solution to this can be written as:
$$
u_{i, j+1} = s(u_{i-1, j} - 2 u_{i, j} + u_{i+1, j}) + 2 u_{i, j} - u_{i, j-1}
$$

where $ s = { {\Delta t^2} \over {\Delta x^2} } $

## References:
- https://en.wikipedia.org/wiki/Wave_equation
- https://en.wikipedia.org/wiki/One-way_wave_equation
- https://github.com/sachabinder/wave_equation_simulations
- Simple explanation:
https://youtu.be/ub7lok-JQJE?si=m7lACwPuZIUp8yYd
- Solving with finite difference technique:
https://youtu.be/CAT2xSaC7UY?si=k2UHA9f9prlaK0XG
- Great explanation of numerical solution:
https://youtu.be/CAT2xSaC7UY?si=ZMJdObqhATR0KMwG
