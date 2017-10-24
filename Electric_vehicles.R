library(plyr)
library(ggplot2)
library(lfe)
library(systemfit)

output<-read.csv("output.csv")

########### Plots ########################
##################################################
### sale ~ charging stations
g<-ggplot(subset(output,State != 'CALIFORNIA' & PHEV == 'True') , aes(N.ChargS,sale))
g+geom_point(aes(color=State))+geom_smooth()

g2<-ggplot(subset(output,State != 'CALIFORNIA' & PHEV == 'False') , aes(N.ChargS,sale))
g2+geom_point(aes(color=State))+geom_smooth()

g3<-ggplot(subset(output,State == 'CALIFORNIA' & PHEV == 'False') , aes(N.ChargS,sale))
g3+geom_point(aes(color=State))+geom_smooth()

g4<-ggplot(subset(output,State == 'CALIFORNIA' & PHEV == 'True') , aes(N.ChargS,sale))
g4+geom_point(aes(color=State))+geom_smooth()

############### SALE (BEV vs PHEV) ~ Charging station

##### creating variables: BEV Sale and PHEV Sale
PHEV_Test<-ifelse(output$PHEV=='True',1,0)
BEV_Test<-ifelse(output$PHEV=='False',1,0)
output2<-mutate(output,PHEV.Sale=sale*PHEV_Test)
output2<-mutate(output2,BEV.Sale=sale*BEV_Test)

ggplot(output, aes(x =N.ChargS , y = sale, colour = PHEV))  +
        stat_smooth(method='loess')

g<-ggplot(output2)
g+geom_smooth(aes(x=N.ChargS,y=BEV.Sale,color='BEV'))+
        geom_smooth(aes(x=N.ChargS,y=PHEV.Sale,color='PHEV'))

d<-ddply(output2,.(t),summarize,PHEV.Sale=mean(PHEV.Sale),BEV.Sale=mean(BEV.Sale),charg.station=mean(N.ChargS))
d
g<-ggplot(d)
g+geom_point(aes(x=t,y=BEV.Sale,color='BEV'))+
        geom_point(aes(x=t,y=charg.station,color='Charging Station'))+
        geom_point(aes(x=t,y=PHEV.Sale,color='PHEV'))+stat_smooth(aes(x=t,y=BEV.Sale,color='BEV'))



output3<-output
levels(output3$PHEV)
levels(output3$PHEV)<-c('BEV','PHEV')

qplot(N.ChargS,sale,data=output3,facets=PHEV~.)+geom_smooth()+
        labs(title='Number of Charging Station vs Sale of EVs')+labs(x='Number of Charging Stations',y="Sale of Evs")

# Plotting logs

output3[output3==0]<-0.1
qplot(log(N.ChargS),log(sale),data=output3,facets=PHEV~.)+geom_smooth()+
        coord_cartesian(ylim=c(0,7.5),xlim=c(0,6.5))+
        labs(title='Number of Charging Station vs Sale of EVs')+labs(x='Number of Charging Stations',y="Sale of Evs")


### sale ~ tax incentive
par(mfrow=c(1,2))
g<-ggplot(subset(output3,State != 'DC' & State!= 'Georgia'& PHEV == 'True') , aes(log(EV.Tax.Inc),log(sale)))
g+geom_point(aes(color=State))+geom_smooth()

g<-ggplot(subset(output,State != 'DC' & State!= 'Georgia'& PHEV == 'False') , aes(EV.Tax.Inc,sale))
g+geom_point(aes(color=State))+geom_smooth()
#### result: not using LOG of tax incentive

### sale ~ income
g3<-ggplot(subset(output3,State != 'CALIFORNIA' & PHEV == 'False') , aes(log(Income),log(sale)))
g3+geom_point(aes(color=State))+geom_smooth()

g4<-ggplot(subset(output,State == 'CALIFORNIA' & PHEV == 'True') , aes(Income,sale))
g4+geom_point(aes(color=State))+geom_smooth()

### sale ~ driving range
## output 3 with logs
g3<-ggplot(subset(output3, PHEV == 'False') , aes(log(D.Range),log(sale)))
g3+geom_point(aes(color=State))+geom_smooth()

g4<-ggplot(subset(output3,PHEV == 'True') , aes(D.Range,log(sale)))
g4+geom_point(aes(color=State))+geom_smooth()

### sale ~ price
g3<-ggplot(subset(output3, PHEV == 'False') , aes(log(PRICE),log(sale)))
g3+geom_point()+geom_smooth()

g4<-ggplot(subset(output3, PHEV == 'True') , aes(PRICE,log(sale)))
g4+geom_point()+geom_smooth()

### price~ driving range
g3<-ggplot(subset(output, PHEV == 'False') , aes(log(PRICE),D.Range))
g3+geom_point()+geom_smooth()

g4<-ggplot(subset(output, PHEV == 'True') , aes(log(PRICE),D.Range))
g4+geom_point()+geom_smooth()

################## finding average of EV sale over MODEL, MAKE, and STATE ########################
d<-ddply(output,.(MODEL),summarize,sale=mean(sale))
arrange(d,desc(sale))
g<-ggplot(d,aes(sale,MODEL))
g+geom_point()

d<-ddply(output,.(MAKE),summarize,sale=mean(sale))
arrange(d,desc(sale))
g<-ggplot(d,aes(sale,MAKE))
g+geom_point()

d<-ddply(output,.(State),summarize,sale=mean(sale))
arrange(d,desc(sale))
g<-ggplot(subset(d,State!='CALIFORNIA'),aes(sale,State))
g+geom_point()


###########################################################################
 # EV Demand Equation
######################### OLS  #########################
f<-lm(log(sale) ~ log(N.ChargS) +Income+ Commute+ Gas.Price+ EV.Tax.Inc + D.Range + PRICE, data=subset(output2, PHEV=='False'))
summary(f)

f<-lm(sale ~ N.ChargS +Income+ Commute+ Gas.Price+ EV.Tax.Inc + D.Range + PRICE, data=subset(output, PHEV=='False'))
summary(f)

#### BEST fit with all logs
fitEV<-lm(log(sale) ~ log(N.ChargS) +log(Income)+ log(Commute)+ log(Gas.Price)+ log(EV.Tax.Inc) + log(D.Range) + log(PRICE), data=subset(output3, PHEV=='False'))
summary(fitEV)

fitPHEV<-lm(log(sale) ~ log(N.ChargS) +log(Income)+ log(Commute)+ log(Gas.Price)+ log(EV.Tax.Inc) + log(D.Range) + log(PRICE), data=subset(output3, PHEV=='True'))
summary(fitPHEV)

par(mfrow=c(2,2))
plot(fit)

f2<-lm(sale ~ N.ChargS +Income+ Commute+ Gas.Price+ EV.Tax.Inc + D.Range + PRICE, data=subset(output2, PHEV=='True'))
summary(f2)

######################### OLS + fixed effects #########################
###########################################################################

#### driving range only varies across models (constant in t and state)
#### using MODEL fixed effects wouldn't work without introducing time-variations

output4<-mutate(output3,new.Range=D.Range-sample(c(0.1,0.2)))

f<-felm(log(sale) ~ log(N.ChargS) +log(Income)+ log(Commute)+ log(Gas.Price) + log(new.Range) + log(PRICE) +log(EV.Tax.Inc) | MODEL + t  , data=subset(output4, PHEV=='False'))
summary(f)
head(output3$D.Range-output4$new.Range)

#### Gas Price only varies across time (constant in all states)
#### using t fixed effects wouldn't work without introducing state-variations

output4<-mutate(output4,new.GasPrice=Gas.Price-sample(c(0.01,0.02,0.03)))

fEV<-felm(log(sale) ~ log(N.ChargS) +log(Income)+ log(Commute)+ log(new.GasPrice) + log(new.Range) + log(PRICE) +log(EV.Tax.Inc) | MODEL + t  , data=subset(output4, PHEV=='False'))
summary(fEV)

fPHEV<-felm(log(sale) ~ log(N.ChargS) +log(Income)+ log(Commute)+ log(new.GasPrice) + log(new.Range) + log(PRICE) +log(EV.Tax.Inc) | MODEL + t  , data=subset(output4, PHEV=='True'))
summary(fPHEV)

#### adding state fixed effects = HYBRID CARS SALE


f<-felm(log(sale) ~ log(N.ChargS) +log(Income)+ log(Commute)+ log(new.GasPrice) + log(new.Range) + log(PRICE) +log(EV.Tax.Inc) + Hybrid.Sales | MODEL + t  , data=subset(output4, PHEV=='False'))
summary(f)


######################## System of Equations ########################

str(output)
eq1<-log(sale)~ log(N.ChargS) +log(Gas.Price) + log(EV.Tax.Inc) + log(Income) + log(PRICE) + log(D.Range) + log(Commute)
eq2<-log(N.ChargS)~ log(BEV.C.Sale)+ Grant.Percent +Infras.Incentive + Hybrid.Sales

# Instruments
inst<- list(~ Infras.Incentive+ Grant.Percent +log(Gas.Price) + log(EV.Tax.Inc) + log(Income)+ log(D.Range) + log(Commute), ~  log(Income) + Grant.Percent +Infras.Incentive + Hybrid.Sales  )
system<-list(eq1=eq1,eq2=eq2) 

reg2sls<-systemfit(system,"2SLS",inst =inst ,data=subset(output3,PHEV=='BEV'))
summary(reg2sls)

reg3sls<-systemfit(system,"3SLS",inst =inst ,data=(output3,PHEV=='BEV'))
summary(reg3sls)

######################## Fixed Effects with Instruments ########################
ev2sls<-felm( log(merged.data$sale) ~log(merged.data$N.ChargS.x)  + log(merged.data$Rebate.x) + log(merged.data$Income.x) + log(merged.data$PRICE) |  MODEL | (log(N.ChargS.x)|log(PRICE)  ~  Grant.Percent.y + Incentive.y))
summary(ev2sls)  

ev2sls<-felm ( log(merged.data$sale) ~log(merged.data$N.ChargS.x) +log(merged.data$Gas.Price.x*trend) + log(merged.data$Rebate.x) + log(merged.data$Income.x) + log(merged.data$PRICE)+log(merged.data$Hybrid.Sales.x)|  merged.data$MODEL |(log(merged.data$N.ChargS.x) ~log(merged.data$Grant.Percent.y)))



