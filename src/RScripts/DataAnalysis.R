# author: Marios

library(ggplot2)
library(reshape)
library(car)
library(sjstats)

# install.packages("ggplot2")
# install.packages("reshape")
# install.packages("car")

# Read the file and remove the uneccessary columns.
data = read.csv("aggregated_data.csv")
data = data[-c(1, 5, 6)]
summary(data)


################################### PLOTTING ###############################################
# We plot boxplots for based on energy_consumption, cpu and mem 
# with respect to web front-end frameworks 
ggplot(data, aes(x=subject, y=energy_consumption)) + 
  geom_boxplot()

ggplot(data, aes(x=subject, y=cpu)) + 
  geom_boxplot()

ggplot(data, aes(x=subject, y=mem))  + 
  geom_boxplot()


# And a combined qqplot with colors on the web front-end framework
p = qplot(sample = energy_consumption, data = data, color=subject)
p + stat_qq(aes(color = subject))
p



#################################### NORMALITY ##############################################
# Additionally, in the same manner we plot qqplots
# to check for normality in our dataset
ggplot(data, aes(sample=energy_consumption))+ stat_qq(distribution = qnorm)
ggplot(data, aes(sample=cpu), ylab("CPU Load")) + stat_qq(distribution = qnorm)
ggplot(data, aes(sample=mem), ylab("Memory Usage")) + stat_qq(distribution = qnorm)

# For extra validation, we conduct shapiro tests
shapiro.test(data$energy_consumption)
shapiro.test(data$cpu)
shapiro.test(data$mem)

# Based on the shapiro tests and the qqplots
# We cannot assume normality across the dataset


########################### Levene Test ######################################################
######### check for homogeneity of variance
leveneTest(energy_consumption ~ subject, data=data)
leveneTest(cpu ~ subject, data=data)
leveneTest(mem ~ subject, data=data)


############################# ANOVA ##########################################################
data$subject = as.factor(data$subject)

modelEnergySubject = lm(energy_consumption~subject, data=data)
anova(modelEnergySubject)
summary(modelEnergySubject)


modelCPU = lm(cpu~subject, data=data)
anova(modelCPU)
summary(modelCPU)


modelMEM = lm(mem~subject, data=data)
anova(modelMEM)
summary(modelMEM)

pairwise.t.test(data$energy_consumption, data$subject,
                p.adjust.method = "BH")

pairwise.t.test(data$cpu, data$subject,
                p.adjust.method = "BH")

pairwise.t.test(data$mem, data$subject,
                p.adjust.method = "BH")


# Plot residuals
par(mfrow=c(1,3))
qqnorm(modelEnergySubject$residuals)
qqnorm(modelCPU$residuals)
qqnorm(modelMEM$residuals)


############################# KRUSKAL WALLIS #################################################
attach(data)

kruskal.test(energy_consumption~subject)
kruskal.test(cpu~subject)
kruskal.test(mem~subject)


pairwise.wilcox.test(energy_consumption, subject,
                     p.adjust.method = "BH")

pairwise.wilcox.test(cpu, subject,
                     p.adjust.method = "BH")

pairwise.wilcox.test(mem, subject,
                     p.adjust.method = "BH")
