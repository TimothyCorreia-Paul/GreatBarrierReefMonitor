# Clean up the environment before starting
rm(list = ls())
install.packages("dplyr")
install.packages("purrr")
#Read csv,name as dt
dt <- read.csv("~/Desktop/can_modify_data.csv")
summary(dt)
#For MEAN_LIVE_CORAL
multireg_MEAN_LIVE_CORAL <- lm(dt$MEAN_LIVE_CORAL ~ 
                                 dt$LATITUDE+dt$LONGITUDE+dt$MEAN_COTS_PER_TOW
     +dt$sample_year+ 
       dt$sample_month +dt$tempreature_aveyearly,data = dt)
multireg_MEAN_LIVE_CORAL
summary(multireg_MEAN_LIVE_CORAL)
multireg_MEAN_LIVE_CORAL_aic = step(multireg_MEAN_LIVE_CORAL)
summary(multireg_MEAN_LIVE_CORAL_aic)
multireg_MEAN_LIVE_CORAL_aic$coefficients

#For MEAN_dead_CORAL #strongly negatively associated with temperature_aveyearly
multireg_MEAN_DEAD_CORAL <- lm(dt$MEAN_DEAD_CORAL ~ 
                                 dt$LATITUDE+dt$LONGITUDE+dt$MEAN_COTS_PER_TOW+
                              +dt$sample_year+ 
                                dt$sample_month +dt$tempreature_aveyearly,data = dt)
multireg_MEAN_DEAD_CORAL
summary(multireg_MEAN_DEAD_CORAL)
multireg_MEAN_DEAD_CORAL_aic = step(multireg_MEAN_DEAD_CORAL)
summary(multireg_MEAN_DEAD_CORAL_aic)
multireg_MEAN_DEAD_CORAL_aic$coefficients

#For MEAN_soft_CORAL
#multireg_MEAN_SOFT_CORAL <- lm(MEAN_SOFT_CORAL ~ 
                                 #LATITUDE+LONGITUDE+MEAN_COTS_PER_TOW
                                  #+sample_year+ 
                                 #sample_month +tempreature_aveyearly,data = dt)
#multireg_MEAN_SOFT_CORAL
#summary(multireg_MEAN_SOFT_CORAL)
#multireg_MEAN_SOFT_CORAL_aic = step(multireg_MEAN_SOFT_CORAL)
#summary(multireg_MEAN_SOFT_CORAL_aic)
#multireg_MEAN_SOFT_CORAL_aic$coefficients

#FOR MEAN_soft_CORAL Found out only LATITUDE, LONGTITUDE, sample_year, sample_month and tempreature_aveyearly is related
multireg_MEAN_SOFT_CORAL <- lm(MEAN_SOFT_CORAL ~ 
                                 dt$LATITUDE+dt$LONGITUDE
                                +dt$sample_year+ 
                                 dt$sample_month +dt$tempreature_aveyearly,data = dt)
summary(multireg_MEAN_SOFT_CORAL)
multireg_MEAN_SOFT_CORAL$coefficients

#For prediction in tempreature_aveyearly called lm_tempreature_aveyearly
lm_tempreature_aveyearly <- lm(tempreature_aveyearly ~ dt$sample_year ,data = dt)
summary(lm_tempreature_aveyearly)
lm_tempreature_aveyearly$coefficients

#For prediction in MEAN_COTS_PER_TOW called lm_MEAN_COTS_PER_TOW
lm_MEAN_COTS_PER_TOW <- lm(MEAN_COTS_PER_TOW ~ 
                                 LATITUDE+LONGITUDE +MEAN_LIVE_CORAL+ MEAN_SOFT_CORAL+ MEAN_DEAD_CORAL+Temperature
                               +sample_year +temperature_aveyearly,data = dt)
summary(lm_MEAN_COTS_PER_TOW)
lm_MEAN_COTS_PER_TOW$coefficients
#________________________________________________________________________________________
library(dplyr)

# Create a data frame with unique REEF_NAME, REEF_ID, LATITUDE, and LONGITUDE from dt
dt_output <- unique(dt[, c("REEF_NAME", "REEF_ID", "LATITUDE", "LONGITUDE")])

# Create a new column for each set of LATITUDE and LONGITUDE with new_sample_year containing 2023, 2024, 2025, 2026, and 2027
dt_output <- dt_output[rep(seq_len(nrow(dt_output)), each = 5), ]
dt_output$new_sample_year <- rep(c(2023, 2024, 2025, 2026, 2027), nrow(dt_output)/5)
# dt_output working__________________________________________________________________________________
# Predict MEAN_COTS_PER_TOW for each row in dt_output using linear regression model lm_MEAN_COTS_PER_TOW
#dt_output$MEAN_COTS_PER_TOW <- predict(lm_MEAN_COTS_PER_TOW, newdata = cbind(dt,dt_output))
MEAN_COTS_PER_TOW_pred <- predict(lm_MEAN_COTS_PER_TOW, newdata = dt_output)




# Predict temperature for each row in dt_output using linear regression model lm_tempreature_aveyearly
dt_output$tempreature_aveyearly <- predict(lm_tempreature_aveyearly, newdata = dt_output)

# Predict percentage of soft coral for each row in dt_output using linear regression model multireg_MEAN_SOFT_CORAL
dt_output$percentage_soft_coral <- predict(multireg_MEAN_SOFT_CORAL, newdata = dt_output)

# Predict percentage of dead coral for each row in dt_output using linear regression model multireg_MEAN_DEAD_CORAL_aic
dt_output$percentage_dead_coral <- predict(multireg_MEAN_DEAD_CORAL_aic, newdata = dt_output)

# Predict percentage of live coral for each row in dt_output using linear regression model multireg_MEAN_LIVE_CORAL_aic
dt_output$percentage_live_coral <- predict(multireg_MEAN_LIVE_CORAL_aic, newdata = dt_output)
