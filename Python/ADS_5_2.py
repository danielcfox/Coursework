
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.2** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-social-network-analysis/resources/yPcBs) course resource._
# 
# ---

# # Assignment 2 - Network Connectivity
# 
# In this assignment you will go through the process of importing and analyzing an internal email communication network between employees of a mid-sized manufacturing company. 
# Each node represents an employee and each directed edge between two nodes represents an individual email. The left node represents the sender and the right node represents the recipient.

# In[1]:

import networkx as nx

# This line must be commented out when submitting to the autograder
#!head email_network.txt


# ### Question 1
# 
# Using networkx, load up the directed multigraph from `email_network.txt`. Make sure the node names are strings.
# 
# *This function should return a directed multigraph networkx graph.*

# In[36]:

def answer_one():
    
    # Your Code Here
    G_en = nx.read_edgelist('email_network.txt', create_using=nx.MultiDiGraph(), data=(('timestamp', int),), delimiter='\t')
    
    return G_en # Your Answer Here

answer_one()


# ### Question 2
# 
# How many employees and emails are represented in the graph from Question 1?
# 
# *This function should return a tuple (#employees, #emails).*

# In[8]:

def answer_two():
        
    # Your Code Here
    G_en = answer_one()
    
    return G_en.number_of_nodes(), G_en.number_of_edges() # Your Answer Here

answer_two()


# ### Question 3
# 
# * Part 1. Assume that information in this company can only be exchanged through email.
# 
#     When an employee sends an email to another employee, a communication channel has been created, allowing the sender to provide information to the receiver, but not vice versa. 
# 
#     Based on the emails sent in the data, is it possible for information to go from every employee to every other employee?
# 
# 
# * Part 2. Now assume that a communication channel established by an email allows information to be exchanged both ways. 
# 
#     Based on the emails sent in the data, is it possible for information to go from every employee to every other employee?
# 
# 
# *This function should return a tuple of bools (part1, part2).*

# In[9]:

def answer_three():
        
    # Your Code Here
    G_en = answer_one()
    
    return nx.is_strongly_connected(G_en), nx.is_weakly_connected(G_en) # Your Answer Here

answer_three()


# ### Question 4
# 
# How many nodes are in the largest (in terms of nodes) weakly connected component?
# 
# *This function should return an int.*

# In[11]:

def answer_four():
        
    # Your Code Here
    G_en = answer_one()
    
    return len(max(nx.weakly_connected_components(G_en), key=len))# Your Answer Here

answer_four()


# ### Question 5
# 
# How many nodes are in the largest (in terms of nodes) strongly connected component?
# 
# *This function should return an int*

# In[12]:

def answer_five():
        
    # Your Code Here
    G_en = answer_one()
    
    return len(max(nx.strongly_connected_components(G_en), key=len))# Your Answer Here
    
answer_five()


# ### Question 6
# 
# Using the NetworkX function strongly_connected_component_subgraphs, find the subgraph of nodes in a largest strongly connected component. 
# Call this graph G_sc.
# 
# *This function should return a networkx MultiDiGraph named G_sc.*

# In[16]:

def answer_six():
        
    # Your Code Here
    G_en = answer_one()
    G_sc = max(nx.strongly_connected_component_subgraphs(G_en), key=len)
    
    return G_sc # Your Answer Here

answer_six()


# ### Question 7
# 
# What is the average distance between nodes in G_sc?
# 
# *This function should return a float.*

# In[17]:

def answer_seven():
        
    # Your Code Here
    G_sc = answer_six()
    
    return nx.average_shortest_path_length(G_sc)# Your Answer Here

answer_seven()


# ### Question 8
# 
# What is the largest possible distance between two employees in G_sc?
# 
# *This function should return an int.*

# In[18]:

def answer_eight():
        
    # Your Code Here
    G_sc = answer_six()
    
    return nx.diameter(G_sc) # Your Answer Here

answer_eight()


# ### Question 9
# 
# What is the set of nodes in G_sc with eccentricity equal to the diameter?
# 
# *This function should return a set of the node(s).*

# In[21]:

def answer_nine():
       
    # Your Code Here
    G_sc = answer_six()
    
    return set(nx.periphery(G_sc)) # Your Answer Here

answer_nine()


# ### Question 10
# 
# What is the set of node(s) in G_sc with eccentricity equal to the radius?
# 
# *This function should return a set of the node(s).*

# In[22]:

def answer_ten():
        
    # Your Code Here
    G_sc = answer_six()
    
    return set(nx.center(G_sc)) # Your Answer Here

answer_ten()


# ### Question 11
# 
# Which node in G_sc is connected to the most other nodes by a shortest path of length equal to the diameter of G_sc?
# 
# How many nodes are connected to this node?
# 
# 
# *This function should return a tuple (name of node, number of satisfied connected nodes).*

# In[25]:

def answer_eleven():
        
    # Your Code Here
    G_sc = answer_six()
    diam = answer_eight()
    
    maxnodes = 0
    for nodefrom in nx.periphery(G_sc):
        numnodes = 0
        for nodeto in G_sc.nodes():
            if (nx.shortest_path_length(G_sc, nodefrom)[nodeto] == diam):
                numnodes = numnodes + 1
        if (numnodes >= maxnodes):
            maxnodes = numnodes
            maxnode = nodefrom
   
    return maxnode, len(G_sc.neighbors(maxnode)) # Your Answer Here

answer_eleven()


# ### Question 12
# 
# Suppose you want to prevent communication from flowing to the node that you found in the previous question from any node in the center of G_sc, what is the smallest number of nodes you would need to remove from the graph (you're not allowed to remove the node from the previous question or the center nodes)? 
# 
# *This function should return an integer.*

# In[29]:

def answer_twelve():
        
    # Your Code Here
    G_sc = answer_six()
    target_node, _ = answer_eleven()
    
    allnodes = set()
    for center_node in nx.center(G_sc):
        nodes = set(nx.minimum_node_cut(G_sc, center_node, target_node))
        allnodes = allnodes.union(nodes)
        
    return len(allnodes) # Your Answer Here

answer_twelve()


# ### Question 13
# 
# Construct an undirected graph G_un using G_sc (you can ignore the attributes).
# 
# *This function should return a networkx Graph.*

# In[34]:

def answer_thirteen():
        
    # Your Code Here
    G_sc = answer_six()
    G_un = nx.Graph(G_sc.to_undirected())
    
    return G_un # Your Answer Here

answer_thirteen()


# ### Question 14
# 
# What is the transitivity and average clustering coefficient of graph G_un?
# 
# *This function should return a tuple (transitivity, avg clustering).*

# In[35]:

def answer_fourteen():
        
    # Your Code Here
    G_un = answer_thirteen()
    
    return nx.transitivity(G_un), nx.average_clustering(G_un) # Your Answer Here

answer_fourteen()


# In[ ]:



