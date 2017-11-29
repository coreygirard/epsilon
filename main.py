from flask import Flask, request, redirect, render_template, Markup, session
from pprint import pprint
import hashlib
import json
import time
import random
import os
import re


class GenerateUUID(object):
    def __init__(self):
        self.s = {}
        self.n = 0

    def get(self,e):
        assert(type(e) == type('string'))
        if e not in self.s.keys():
            self.s[e] = self.n
            self.n += 1

        return self.s[e]

    def query(self,e):
        print(e)
        assert(type(e) == type('string'))
        if e in self.s.keys():
            return self.s[e]
        else:
            return None

class Doc(object):
    def __init__(self,ids):
        self.ids = ids
        self.counter = {}
        for i in ids:
            self.counter[i] = self.counter.get(i,0)+1

class DB(object):
    def __init__(self):
        self.uuid = GenerateUUID()
        self.doc = {}

    def parse(self,s):
        s = re.sub(r'[\[].*?[\]]',r'',s)
        s = s.split(' ')
        return Doc([self.uuid.get(e) for e in s])

    def addDoc(self,k,v):
        self.doc[k] = self.parse(v)

    def queryWord(self,q):
        results = {}
        for k,v in self.doc.items():
            n = v.counter.get(q,0)
            if n != 0:
                results[k] = n/sum(v.counter.values())

        return results

    def query(self,q):
        q = [self.uuid.query(w) for w in q.split(' ')]

        results = [self.queryWord(w) for w in q]

        s = set(results[0].keys())
        for i in range(1,len(results)):
            s = s & set(results[i].keys())

        score = {e:1.0 for e in s}
        for result in results:
            for k in score.keys():
                score[k] *= result[k]

        return sorted(list(score.items()),key=lambda x : -x[1])[:10]

db = DB()

#with open('raw.json','r') as f:
#    raw = json.load(f)

raw = {
    "Game_theory": "Game theory is \"the study of mathematical models of conflict and cooperation between intelligent rational decision-makers\". Game theory is mainly used in economics, political science, and psychology, as well as logic, computer science and biology.[1] Originally, it addressed zero-sum games, in which one person's gains result in losses for the other participants. Today, game theory applies to a wide range of behavioral relations, and is now an umbrella term for the science of logical decision making in humans, animals, and computers. Modern game theory began with the idea regarding the existence of mixed-strategy equilibria in two-person zero-sum games and its proof by John von Neumann. Von Neumann's original proof used the Brouwer fixed-point theorem on continuous mappings into compact convex sets, which became a standard method in game theory and mathematical economics. His paper was followed by the 1944 book Theory of Games and Economic Behavior, co-written with Oskar Morgenstern, which considered cooperative games of several players. The second edition of this book provided an axiomatic theory of expected utility, which allowed mathematical statisticians and economists to treat decision-making under uncertainty. This theory was developed extensively in the 1950s by many scholars. Game theory was later explicitly applied to biology in the 1970s, although similar developments go back at least as far as the 1930s. Game theory has been widely recognized as an important tool in many fields. With the Nobel Memorial Prize in Economic Sciences going to game theorist Jean Tirole in 2014, eleven game-theorists have now won the economics Nobel Prize. John Maynard Smith was awarded the Crafoord Prize for his application of game theory to biology.",
    "Decision_theory": "Decision theory (or the theory of choice) is the study of the reasoning underlying an agent's choices.[1] Decision theory can be broken into two branches: normative decision theory, which gives advice on how to make the best decisions, given a set of uncertain beliefs and a set of values; and descriptive decision theory, which analyzes how existing, possibly irrational agents actually make decisions. Closely related to the field of game theory,[2] decision theory is concerned with the choices of individual agents whereas game theory is concerned with interactions of agents whose decisions affect each other. Decision theory is an interdisciplinary topic, studied by economists, statisticians, psychologists, biologists,[3] political and other social scientists, philosophers,[4] and computer scientists. Empirical applications of this rich theory are usually done with the help of statistical and econometric methods, especially via the so-called choice models, such as probit and logit models. Estimation of such models is usually done via parametric, semi-parametric and non-parametric maximum likelihood methods.[5]",
    "Mathematics": "Mathematics (from Greek \u03bc\u03ac\u03b8\u03b7\u03bc\u03b1 m\u00e1th\u0113ma, \"knowledge, study, learning\") is the study of objects and their relations. Examples of objects are quantity (numbers),[1] structure,[2] space,[1] and change.[3][4][5] There is a range of views among mathematicians and philosophers as to the exact scope and definition of mathematics.[6][7] Mathematicians seek out patterns[8][9] and use them to formulate new conjectures. Mathematicians resolve the truth or falsity of conjectures by mathematical proof. When mathematical structures are good models of real phenomena, then mathematical reasoning can provide insight or predictions about nature. Through the use of abstraction and logic, mathematics developed from counting, calculation, measurement, and the systematic study of the shapes and motions of physical objects. Practical mathematics has been a human activity from as far back as written records exist. The research required to solve mathematical problems can take years or even centuries of sustained inquiry. Rigorous arguments first appeared in Greek mathematics, most notably in Euclid's Elements. Since the pioneering work of Giuseppe Peano (1858\u20131932), David Hilbert (1862\u20131943), and others on axiomatic systems in the late 19th century, it has become customary to view mathematical research as establishing truth by rigorous deduction from appropriately chosen axioms and definitions. Mathematics developed at a relatively slow pace until the Renaissance, when mathematical innovations interacting with new scientific discoveries led to a rapid increase in the rate of mathematical discovery that has continued to the present day.[10][page needed] Galileo Galilei (1564\u20131642) said, \"The universe cannot be read until we have learned the language and become familiar with the characters in which it is written. It is written in mathematical language, and the letters are triangles, circles and other geometrical figures, without which means it is humanly impossible to comprehend a single word. Without these, one is wandering about in a dark labyrinth.\"[11] Carl Friedrich Gauss (1777\u20131855) referred to mathematics as \"the Queen of the Sciences\".[12][page needed] Benjamin Peirce (1809\u20131880) called mathematics \"the science that draws necessary conclusions\".[13] David Hilbert said of mathematics: \"We are not speaking here of arbitrariness in any sense. Mathematics is not like a game whose tasks are determined by arbitrarily stipulated rules. Rather, it is a conceptual system possessing internal necessity that can only be so and by no means otherwise.\"[14][page needed] Albert Einstein (1879\u20131955) stated that \"as far as the laws of mathematics refer to reality, they are not certain; and as far as they are certain, they do not refer to reality.\"[15] Mathematics is essential in many fields, including natural science, engineering, medicine, finance and the social sciences. Applied mathematics has led to entirely new mathematical disciplines, such as statistics and game theory. Mathematicians also engage in pure mathematics, or mathematics for its own sake, without having any application in mind. There is no clear line separating pure and applied mathematics, and practical applications for what began as pure mathematics are often discovered.[16][page needed]",
    "Statistics": "Statistics is a branch of mathematics dealing with the collection, analysis, interpretation, presentation, and organization of data.[1][2] In applying statistics to, e.g., a scientific, industrial, or social problem, it is conventional to begin with a statistical population or a statistical model process to be studied. Populations can be diverse topics such as \"all people living in a country\" or \"every atom composing a crystal.\" Statistics deals with all aspects of data including the planning of data collection in terms of the design of surveys and experiments.[1] When census data cannot be collected, statisticians collect data by developing specific experiment designs and survey samples. Representative sampling assures that inferences and conclusions can reasonably extend from the sample to the population as a whole. An experimental study involves taking measurements of the system under study, manipulating the system, and then taking additional measurements using the same procedure to determine if the manipulation has modified the values of the measurements. In contrast, an observational study does not involve experimental manipulation. Two main statistical methods are used in data analysis: descriptive statistics, which summarize data from a sample using indexes such as the mean or standard deviation, and inferential statistics, which draw conclusions from data that are subject to random variation (e.g., observational errors, sampling variation).[3] Descriptive statistics are most often concerned with two sets of properties of a distribution (sample or population): central tendency (or location) seeks to characterize the distribution's central or typical value, while dispersion (or variability) characterizes the extent to which members of the distribution depart from its center and each other. Inferences on mathematical statistics are made under the framework of probability theory, which deals with the analysis of random phenomena. A standard statistical procedure involves the test of the relationship between two statistical data sets, or a data set and synthetic data drawn from idealized model. A hypothesis is proposed for the statistical relationship between the two data sets, and this is compared as an alternative to an idealized null hypothesis of no relationship between two data sets. Rejecting or disproving the null hypothesis is done using statistical tests that quantify the sense in which the null can be proven false, given the data that are used in the test. Working from a null hypothesis, two basic forms of error are recognized: Type I errors (null hypothesis is falsely rejected giving a \"false positive\") and Type II errors (null hypothesis fails to be rejected and an actual difference between populations is missed giving a \"false negative\").[4] Multiple problems have come to be associated with this framework: ranging from obtaining a sufficient sample size to specifying an adequate null hypothesis.[citation needed] Measurement processes that generate statistical data are also subject to error. Many of these errors are classified as random (noise) or systematic (bias), but other types of errors (e.g., blunder, such as when an analyst reports incorrect units) can also be important. The presence of missing data or censoring may result in biased estimates and specific techniques have been developed to address these problems. Statistics can be said to have begun in ancient civilization, going back at least to the 5th century BC, but it was not until the 18th century that it started to draw more heavily from calculus and probability theory.",
    "Systems_theory": "Systems theory is the interdisciplinary study of systems. A system is an entity with interrelated and interdependent parts; it is defined by its boundaries and it is more than the sum of its parts (subsystem). Changing one part of the system affects other parts and the whole system, with predictable patterns of behavior. Positive growth and adaptation of a system depend upon how well the system is adjusted with its environment, and systems often exist to accomplish a common purpose (a work function) that also aids in the maintenance of the system or the operations may result in system failure. The goal of systems theory is systematically discovering a system's dynamics, constraints, conditions and elucidating principles (purpose, measure, methods, tools, etc.) that can be discerned and applied to systems at every level of nesting, and in every field for achieving optimized equifinality.[1] General systems theory is about broadly applicable concepts and principles, as opposed to concepts and principles applicable to one domain of knowledge. It distinguishes dynamic or active systems from static or passive systems. Active systems are activity structures or components that interact in behaviours and processes. Passive systems are structures and components that are being processed. E.g. a program is passive when it is a disc file and active when it runs in memory.[2] The field is related to systems thinking and systems engineering.",
    "Information_theory": "Information theory studies the quantification, storage, and communication of information. It was originally proposed by Claude E. Shannon in 1948 to find fundamental limits on signal processing and communication operations such as data compression, in a landmark paper entitled \"A Mathematical Theory of Communication\". Applications of fundamental topics of information theory include lossless data compression (e.g. ZIP files), lossy data compression (e.g. MP3s and JPEGs), and channel coding (e.g. for digital subscriber line (DSL)). Its impact has been crucial to the success of the Voyager missions to deep space, the invention of the compact disc, the feasibility of mobile phones, the development of the Internet, the study of linguistics and of human perception, the understanding of black holes, and numerous other fields. A key measure in information theory is \"entropy\". Entropy quantifies the amount of uncertainty involved in the value of a random variable or the outcome of a random process. For example, identifying the outcome of a fair coin flip (with two equally likely outcomes) provides less information (lower entropy) than specifying the outcome from a roll of a die (with six equally likely outcomes). Some other important measures in information theory are mutual information, channel capacity, error exponents, and relative entropy. The field is at the intersection of mathematics, statistics, computer science, physics, neurobiology, and electrical engineering. The theory has also found applications in other areas, including statistical inference, natural language processing, cryptography, neurobiology,[1] the evolution[2] and function[3] of molecular codes (bioinformatics), model selection in statistics,[4] thermal physics,[5] quantum computing, linguistics, plagiarism detection,[6] pattern recognition, and anomaly detection.[7] Important sub-fields of information theory include source coding, channel coding, algorithmic complexity theory, algorithmic information theory, information-theoretic security, and measures of information.",
    "Logic": "Logic (from the Ancient Greek: \u03bb\u03bf\u03b3\u03b9\u03ba\u03ae, translit. logik\u1e17[1]), originally meaning \"the word\" or \"what is spoken\" (but coming to mean \"thought\" or \"reason\"), is generally held to consist of the systematic study of the form of valid inference. A valid inference is one where there is a specific relation of logical support between the assumptions of the inference and its conclusion. (In ordinary discourse, inferences may be signified by words like therefore, hence, ergo and so on. There is no universal agreement as to the exact scope and subject matter of logic (see \u00a7 Rival conceptions, below), but it has traditionally included the classification of arguments, the systematic exposition of the 'logical form' common to all valid arguments, the study of inference, including fallacies, and the study of semantics, including paradoxes. Historically, logic has been studied in philosophy (since ancient times) and mathematics (since the mid-19th century), and recently logic has been studied in computer science, linguistics, psychology, and other fields.",
    "Theoretical_computer_science": "Theoretical computer science, or TCS, is a subset of general computer science and mathematics that focuses on more mathematical topics of computing and includes the theory of computation. It is difficult to circumscribe the theoretical areas precisely. The ACM's Special Interest Group on Algorithms and Computation Theory (SIGACT) provides the following description:[1] TCS covers a wide variety of topics including algorithms, data structures, computational complexity, parallel and distributed computation, probabilistic computation, quantum computation, automata theory, information theory, cryptography, program semantics and verification, machine learning, computational biology, computational economics, computational geometry, and computational number theory and algebra. Work in this field is often distinguished by its emphasis on mathematical technique and rigor. In this list, the ACM's journal Transactions on Computation Theory includes coding theory and computational learning theory, as well as theoretical computer science aspects of areas such as databases, information retrieval, economic models, and networks.[2] Despite this broad scope, the \"theory people\" in computer science self-identify as different from the \"applied people\"[citation needed]. Some characterize themselves as doing the \"(more fundamental) 'science(s)' underlying the field of computing.\"[3] Other \"theory-applied people\" suggest that it is impossible to separate theory and application. This means that the so-called \"theory people\" regularly use experimental science(s) done in less-theoretical areas such as software system research[citation needed]. It also means that there is more cooperation than mutually exclusive competition between theory and application[citation needed].",
    "Control_theory": "Control theory in control systems engineering deals with the control of continuously operating dynamical systems in engineered processes and machines. The objective is to develop a control model for controlling such systems using a control action in an optimum manner without delay or overshoot and ensuring control stability. To do this, a controller with the requisite corrective behaviour is required. This controller monitors the controlled process variable (PV), and compares it with the reference or set point (SP). The difference between actual and desired value of the process variable, called the error signal, or SP-PV error, is applied as feedback to generate a control action to bring the controlled process variable to the same value as the set point. Other aspects which are also studied are controllability and observability. On this is based the advanced type of automation that revolutionized manufacturing, aircraft, communications and other industries. This is feedback control, which is usually continuous and involves taking measurements using a sensor and making calculated adjustments to keep the measured variable within a set range by means of a \"final control element\", such as a control valve.[1] Extensive use is usually made of a diagrammatic style known as the block diagram. In it the transfer function, also known as the system function or network function, is a mathematical model of the relation between the input and output based on the differential equations describing the system. Control theory dates from the 19th century, when the theoretical basis for the operation of governors was first described by James Clerk Maxwell.[2] Control theory was further advanced by Edward Routh in 1874, Charles Sturm and in 1895, Adolf Hurwitz, who all contributed to the establishment of control stability criteria; and from 1922 onwards, the development of PID control theory by Nicolas Minorsky.[3] Although a major application of control theory is in control systems engineering, which deals with the design of process control systems for industry, other applications range far beyond this. As the general theory of feedback systems, control theory is useful wherever feedback occurs. A few examples are in physiology, electronics, climate modeling, machine design, ecosystems, navigation, neural networks, predator\u2013prey interaction, gene expression, and production theory.[4]"
}

for k,v in raw.items():
    db.addDoc(k,v)



app = Flask(__name__)

@app.route('/')
def home():
    query = request.args.get('q')

    return '\n'.join([re.sub('_',' ',result.title()) for result,score in db.query('theory')])

if __name__ == '__main__':
    app.run(debug=True)
