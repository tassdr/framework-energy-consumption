# author: Marios

library(ggplot2)
library(reshape)

# install.packages("ggplot2")
# install.packages("reshape")

# Read the file and remove the first column which is uneccessary.
data = read.csv("aggregated_data.csv")
data = data[-c(1)]


# We plot boxplots for based on energy_consumption, cpu and mem 
# with respect to web front-end frameworks 
ggplot(data, aes(x=subject, y=energy_consumption)) + 
  geom_boxplot()

ggplot(data, aes(x=subject, y=cpu)) + 
  geom_boxplot()

ggplot(data, aes(x=subject, y=mem))  + 
  geom_boxplot()

# coord_cartesian(ylim = c(2400000, max(data["mem"])))

# Additionally, in the same manner we plot qqplots
ggplot(data, aes(sample=energy_consumption))+stat_qq()
ggplot(data, aes(sample=cpu)) +stat_qq()
ggplot(data, aes(sample=mem)) +stat_qq()

# And a combined qqplot with colors on the web front-end framework
p = qplot(sample = energy_consumption, data = data, color=subject)
p + stat_qq(aes(color = subject))
p


