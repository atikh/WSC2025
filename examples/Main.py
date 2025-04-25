import sys

sys.path.append('C:/Users/iu4647/Models/05. WSC2025/04.Simulation/14.02.2025')

#########################/
## Imports ##
#########################
from components.spn import *
from components.spn_simulate import simulate
from components.spn_visualization import *
from components.spn import SPN



## Define Dimensions and return to all ##
#########################
Total_Dimensions = ['time', 'Energy', 'Plastic Waste']

if __name__ == "__main__":
    spn = SPN()

#########################
## Define Places
#########################
    p0 = Place("p0")

    pI1 = Place("pI1",1, DoT=1, dimension_tracked="Energy")
    pI2 = Place("pI2", 1, DoT=1, dimension_tracked="Energy")

    p11 = Place("P11")
    p12 = Place("P12")
    p13 = Place("P13")

    p21 = Place("P21")
    p22 = Place("P22")
    p23 = Place("P23")

#########################
## Define Transitions
#########################
    Mt00 = Transition("New Task","T", input_transition=True)

    #Line1
    Mt10 = Transition("Assign the line1", "I")

    Mt11 = Transition("Preprocessing1 (Begin)","I", Join=1)
    Mt11.add_dimension_change("Energy", "rate", 0.50)
    def guard_Mt11():  # check if Robot1 is available
        if len(pI1.n_tokens) >= 1:
            return True
        else:
            return False
    Mt11.set_guard_function(guard_Mt11)

    Mt12 = Transition("Processing1 (Begin)", "T", Fork=1)
    Mt12.add_dimension_change("Energy", "rate", 2)
    Mt12.add_dimension_change("Plastic Waste", "fixed",  0.2)

    Mt13 = Transition("Task Completed1", "I", output_transition=True)

    #Line2

    Mt20 = Transition("Assign the line2", "I")

    Mt21 = Transition("Preprocessing2 (Begin)","I", Join=1)
    Mt21.add_dimension_change("Energy", "rate", 0.37)
    def guard_Mt21():  # check if Robot1 is available
        if len(pI2.n_tokens) >= 1:
            return True
        else:
            return False
    Mt11.set_guard_function(guard_Mt21)

    Mt22 = Transition("Processing2 (Begin)", "T", Fork=1)
    Mt22.add_dimension_change("Energy", "rate", 1.5)
    Mt22.add_dimension_change("Plastic Waste", "fixed",  0.15)

    Mt23 = Transition("Task Completed2", "I", output_transition=True)


    #arrange the transition's settings
    Mt10.set_weight(0.5)
    Mt20.set_weight(0.5)

    Mt00.set_distribution("weibull_min", 0.966320710626624, 0.198000000000000, 9.452523274729678)

    Mt12.set_distribution("norm", 4.908477611940298, 0.334090762456067)
    Mt22.set_distribution("lognorm", 0.131453010051039, 3.004370246373232, 1.974260533976333)


#########################
##     ADD PLACES      ##
#########################
    spn.add_place(p0)
    spn.add_place(pI1)
    spn.add_place(p11)
    spn.add_place(p12)
    spn.add_place(p13)
    spn.add_place(pI2)
    spn.add_place(p21)
    spn.add_place(p22)
    spn.add_place(p23)


#########################
##   ADD Transitions   ##
#########################
    spn.add_transition(Mt00)
    spn.add_transition(Mt10)
    spn.add_transition(Mt11)
    spn.add_transition(Mt12)
    spn.add_transition(Mt13)
    spn.add_transition(Mt20)
    spn.add_transition(Mt21)
    spn.add_transition(Mt22)
    spn.add_transition(Mt23)


#########################
##      ADD links      ##
#########################
    spn.add_output_arc(Mt00,p0)
    spn.add_input_arc(p0,Mt10)
    spn.add_input_arc(p0,Mt20)
    #line1
    spn.add_output_arc(Mt10, p11)
    spn.add_input_arc(p11,Mt11)
    spn.add_input_arc(pI1,Mt11)
    spn.add_output_arc(Mt11, p12)
    spn.add_input_arc(p12,Mt12)
    spn.add_output_arc(Mt12, p13)
    spn.add_output_arc(Mt12, pI1)
    spn.add_input_arc(p13,Mt13)
    # line2
    spn.add_output_arc(Mt20, p21)
    spn.add_input_arc(p21,Mt21)
    spn.add_input_arc(pI2,Mt21)
    spn.add_output_arc(Mt21, p22)
    spn.add_input_arc(p22,Mt22)
    spn.add_output_arc(Mt22, p23)
    spn.add_output_arc(Mt22, pI2)
    spn.add_input_arc(p23,Mt23)

#########################
## Simulation Settings ##
#########################
    simulate(spn, max_time=1440, verbosity=2, protocol=True)

#print_petri_net(spn)
    draw_spn(spn, show=True)


