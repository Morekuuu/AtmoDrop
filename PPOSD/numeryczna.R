library(dplyr)
library(lubridate)

# 1. Wczytanie danych

df <- read.csv('dane_z_chmurami.csv', stringsAsFactors = FALSE)

# 2. Wektoryzacja
df <- df[ order(df[["Height..m."]]), ]
heights  <- df$`Height..m.`
temps     <- df$`Temperature...C.`
humidity  <- df$`Humidity...`

# 3. Punkt rosy
dew_point <- function(T, RH) {
  a <- 17.27
  b <- 237.7
  alpha <- (a * T / (b + T)) + log(RH / 100)
  (b * alpha) / (a - alpha)
}

# 4. Parametry początkowe
step   <- 100   # krok [m]
x      <- 0     # start na 0 m
# temperatura cząstki = temperatura otoczenia na 0 m
T_part <- temps[which(heights == x)]
RH_val <- humidity[which(heights == x)]
dew    <- dew_point(T_part, RH_val)

# 5. Szukanie podstawy chmury
while (T_part > dew) {
  x <- x + step
  T_part <- T_part - 1   # adiabatyczny spadek o 1 °C na 100 m
  
  # pobierz warunki na nowej wysokości (ew. interpoluj)
  if (x %in% heights) {
    idx   <- which(heights == x)
    T_env <- temps[idx]
    RH_val <- humidity[idx]
  } else {
    T_env  <- approx(heights, temps,    xout = x)$y
    RH_val <- approx(heights, humidity, xout = x)$y
  }
  
  dew <- dew_point(T_env, RH_val)
}

cloud_base <- x
cat(sprintf("Podstawa chmury: %d m\n", cloud_base))

# 6. Szukanie wierzchołka chmury
#    w chmurze spadek 0.6 °C na 100 m
T_part <- dew
x       <- cloud_base

repeat {
  x <- x + step
  T_part <- T_part - 0.6
  
  if (x %in% heights) {
    T_env <- temps[which(heights == x)]
  } else {
    T_env <- approx(heights, temps, xout = x)$y
  }
  
  if (T_part <= T_env) {
    cloud_top <- x
    break
  }
}

cat(sprintf("Wierzchołek chmury: %d m\n", cloud_top))

#Tabelka na dane chmurkowe
dfp <- data.frame(cloud_base, cloud_top, H)
dfp

#modelowanie opadów
sigmoid <- function(x) 1 / (1 + exp(-x))


rain_deterministic <- function(dfp,
                               pars = list(
                                 a0 = -3, a1 = 2,        # logistyka
                                 b0 = 0.8, b1 = 1.3,     # intensywność
                                 H0 = 0,                 # KM!!
                                 p_thr = 0.5             # próg klasyfikacji
                               )) {
  
 
  # prawdopodobieństwo opadów
  z <- with(dfp, pars$a0 + pars$a1 * H)   # H zakładamy w [km] już w dfp
  dfp$P_rain <- sigmoid(z)                # dopisujemy do ramki danych
  
  # intensywność opadów - R
  dfp$R <- with(dfp, ifelse(
    (H > pars$H0) & (P_rain > pars$p_thr),
    pars$b0 * (H - pars$H0) ^ pars$b1,
    0
    
  ))
  
  return(dfp)
}

if (interactive()) {
  
  print(result[, c("cloud_base", "cloud_top", "H", "P_rain", "R")], digits = 3)
}

# 1. Wczytaj profil startowy z pliku CSV
df <- read.csv('dane_z_chmurami.csv', stringsAsFactors = FALSE)
df <- df[order(df[["Height..m."]]), ]
heights  <- df$`Height..m.`
temps    <- df$`Temperature...C.`
humidity <- df$`Humidity...`

profile_now <- data.frame(
  height = heights,
  temp   = temps,
  hum    = humidity
)

# 2.Rosa
dew_point <- function(T, RH) {
  a <- 17.27
  b <- 237.7
  alpha <- (a * T / (b + T)) + log(RH / 100)
  (b * alpha) / (a - alpha)
}

# 3. Trendy dziennej zmiany temperatury i wilgotności 
get_trend <- function(hour_utc) {
  if (hour_utc %in% c(0, 3, 6))      return(list(dT = 2/12, dH = -10/12))
  else if (hour_utc %in% c(9, 12, 15)) return(list(dT = 1/12, dH = -10/12))
  else if (hour_utc %in% c(18, 21))    return(list(dT = -2/12, dH = +10/12))
  else                                 return(list(dT = 0, dH = 0))
}

# 4. Funkcja analizy chmurowej (podstawa/wierzchołek/H)
cloud_profile_analysis <- function(profile) {
  step <- 100
  x <- 0
  T_parcel <- profile$temp[which(profile$height == x)]
  RH_val   <- profile$hum[which(profile$height == x)]
  T_env    <- T_parcel
  dew      <- dew_point(T_env, RH_val)
  
  # Szukanie podstawy chmury
  while (TRUE) {
    if (abs(T_parcel - dew) < 1e-2) {
      cloud_base <- x
      break
    }
    x <- x + step
    if (x > max(profile$height)) {
      cloud_base <- NA
      break
    }
    T_env  <- approx(profile$height, profile$temp, xout = x)$y
    RH_val <- approx(profile$height, profile$hum, xout = x)$y
    T_parcel <- T_parcel - 1.0
    dew <- dew_point(T_env, RH_val)
  }
  
  # Szukanie wierzchołka chmury
  if (is.na(cloud_base)) {
    cloud_top <- NA
    H <- NA
  } else {
    T_env <- approx(profile$height, profile$temp, xout = cloud_base)$y
    T_parcel <- dew
    x <- cloud_base
    repeat {
      x <- x + step
      if (x > max(profile$height)) {
        cloud_top <- NA
        break
      }
      T_env <- approx(profile$height, profile$temp, xout = x)$y
      T_parcel <- T_parcel - 0.6
      if (T_parcel <= T_env) {
        cloud_top <- x
        break
      }
    }
    H <- if (!is.na(cloud_top)) (cloud_top - cloud_base)/1000 else NA
  }
  data.frame(cloud_base=cloud_base, cloud_top=cloud_top, H=H)
}

# 5. Funkcja sigmoid i model opadu
sigmoid <- function(x) 1 / (1 + exp(-x))

rain_deterministic <- function(dfp,
                               pars = list(
                                 a0 = -3, a1 = 2,
                                 b0 = 0.8, b1 = 1.3,
                                 H0 = 0,
                                 p_thr = 0.5
                               )) {
  z <- with(dfp, pars$a0 + pars$a1 * H)
  dfp$P_rain <- sigmoid(z)
  dfp$R <- with(dfp, ifelse(
    (H > pars$H0) & (P_rain > pars$p_thr),
    pars$b0 * (H - pars$H0) ^ pars$b1,
    0
  ))
  return(dfp)
}

# 6. Parametry startowe prognozy
start_datetime <- as.POSIXct(now(), tz="UTC")  # lub podaj konkretną godzinę
start_hour     <- hour(start_datetime)
lead_hours     <- c(3, 6, 9, 12)

# 7. Dla każdej godziny prognozy: licz chmury i opad
results <- data.frame()
for (lead in lead_hours) {
  future_time <- start_datetime + hours(lead)
  trend <- get_trend(start_hour)
  dT   <- trend$dT * lead
  dHum <- trend$dH * lead
  
  profile_future <- profile_now
  profile_future$temp <- profile_now$temp + dT
  profile_future$hum  <- pmin(pmax(profile_now$hum + dHum, 0), 100)
  
  chmura <- cloud_profile_analysis(profile_future)
  chmura$godzina_pomiaru  <- start_hour
  chmura$lead_hours       <- lead
  chmura$godzina_prognozy <- hour(future_time)
  
  # Opad i prawdopodobieństwo
  chmura <- rain_deterministic(chmura)
  
  results <- rbind(results, chmura)
}

# 8. Tabela
print(results[, c("godzina_pomiaru", "lead_hours", "godzina_prognozy",
                  "cloud_base", "cloud_top", "H", "P_rain", "R")], digits=3)


# 1. Czas
current_time <- as.POSIXct(now(), tz="UTC")
rok     <- as.integer(format(current_time, "%Y"))
miesiac <- as.integer(format(current_time, "%m"))
dzien   <- as.integer(format(current_time, "%d"))
godzina <- as.integer(format(current_time, "%H"))
minuta  <- as.integer(format(current_time, "%M"))

# 2. Prognoza godzinowa
p3  <- results$R[results$lead_hours == 3]
p6  <- results$R[results$lead_hours == 6]
p9  <- results$R[results$lead_hours == 9]
p12 <- results$R[results$lead_hours == 12]

# 3. Format tabelki
tabelka <- data.frame(
  rok = rok,
  miesiac = miesiac,
  dzien = dzien,
  godzina = godzina,
  minuta = minuta,
  p3 = ifelse(length(p3)>0, p3, NA),
  p6 = ifelse(length(p6)>0, p6, NA),
  p9 = ifelse(length(p9)>0, p9, NA),
  p12 = ifelse(length(p12)>0, p12, NA)
)

tabelka[is.na(tabelka)] <- 0
tabelka
write.csv(tabelka, file = "prognoza_opadow.csv", row.names = FALSE)
