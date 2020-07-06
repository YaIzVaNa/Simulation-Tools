# Simulation Tools
A compendium of different tools developed for process optimization. So far this repository includes

  - <b>Calculate Jacobian </b> (JacobianCalc.py) - Input a symbolic mathematical expression, can be a list of equations. Output the Jacobian. Useful for automating the generation of process constraints which require sensitivity information. The purpose of the script is to symbolically calculate the first order derivative of four different expressions: 
  
        1. Objective function
        2. Simple constraint
        3. Indexed constraint
        4. Indexed constraint with indexed variables
        
- <b>Ipopt/COINOR compilation tutorial </b> - Will help the user step-by-step on the following points:

        1. Compilation of COINOR solvers
        2. How to replace the default linear solvers with an academic license of the HSL solvers
        3. Troubleshooting and compilation errors

