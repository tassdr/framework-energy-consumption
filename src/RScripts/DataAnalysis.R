# 
library(ggplot2)

data = read.csv("aggregated_data.csv")
data = data[-c(1)]



ggplot(data, aes(x=subject, y=energy_consumption)) + 
  geom_boxplot()

ggplot(data, aes(x=subject, y=cpu)) + 
  geom_boxplot()

ggplot(data, aes(x=subject, y=mem))  + 
  geom_boxplot()

# coord_cartesian(ylim = c(2400000, max(data["mem"])))

tmp = data["subject"] == "react-redux"
qqnorm(data[tmp, "energy_consumption"])
shapiro.test(data[tmp, "energy_consumption"])


qqnorm(data$energy_consumption)


shapiro.test(data$energy_consumption)



energy = data["energy_consumption"]
qnorm(energy)
