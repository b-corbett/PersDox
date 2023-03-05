import mathgenerator
import args

if __name__ == "__main__":
	args = sys.argv 		# <script_name> <solver_name> [<test_pairs>]
    solver = args[1]

    genList = mathgenerator.getGenList()
    for gen_prob in genList:
        if gen_prob[3] == solver:
            print(gen_prob[4])
