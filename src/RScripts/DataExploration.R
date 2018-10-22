# author: Marios


# First we change the directory to the aggregated_results,
# where all the csv files from each experiment lie inside. 
getwd()
setwd("Aggregated_Results")

# We load up all the different datasets, from each experiment, in a list.
experimentFilenames = list.files(pattern="*.csv")
data = lapply(experimentFilenames, read.csv)

# We reset the working directory back to normal.
setwd("..")
getwd()


# Here, for each web front-end framework dataset we acquire only the columns that are important 
# for our statistical analysis and after we change the column names for convinience.
# Additionally, we convert "battery" from uWatt to Watt using lapply.
# Moreover, we create a column "Energy consumption" 
# which is the product of "duration(seconds)" and "battery(Watts)"
# Finally we round all numeric elements down to 3-digits

cols = c("subject", "CPU.Load....", "Memory.Usage..KB.", "duration.s.", "Battery.Power...uW.")
newnames = c("subject", "cpu", "mem", "duration", "battery")

for (i in 1:length(data))
{
  data[[i]] = data[[i]][cols]
  colnames(data[[i]]) = newnames
  data[[i]]["battery"] = lapply(data[[i]]["battery"], function(row_val) row_val / 1e+6)
  data[[i]]["energy_consumption"] = data[[i]]["duration"] * data[[i]]["battery"]
}


# Merge all our experiments into one data frame, 
# round the digits to 3 
# and save it as a csv file

finalDataframe = do.call(what = rbind, args = data)
numeric_columns = sapply(finalDataframe, class) == 'numeric'
finalDataframe[numeric_columns] = round (finalDataframe[numeric_columns], digits = 3)
write.csv(finalDataframe, file="aggregated_data.csv")
