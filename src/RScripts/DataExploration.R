df = read.csv("aggregated_results.csv")

colnames(df)

cols = c("subject", "CPU.Load....", "Memory.Usage..KB.", "duration.s.", "Battery.Power...uW.")
angularjs = df[cols]


newnames = c("subject", "cpu", "mem", "duration", "battery")
colnames(angularjs) = newnames


