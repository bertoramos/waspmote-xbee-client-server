
void clearINT() {
  PWR.clearInterruptionPin();
  clearIntFlag();
}

void set_unixtime(unsigned long unixtime)
{
  timestamp_t rtc_timestamp;
  
  RTC.breakTimeAbsolute( unixtime, &rtc_timestamp ); 
  int yy = rtc_timestamp.year;
  int mm = rtc_timestamp.month;
  int dd = rtc_timestamp.date;
  int HH = rtc_timestamp.hour;
  int MM = rtc_timestamp.minute;
  int SS = rtc_timestamp.second;
  uint8_t day_of_week = RTC.dow(yy,mm,dd);
  
  char buf[80];
  
  sprintf(buf, "%02d:%02d:%02d:%02d:%02d:%02d:%02d", yy, mm, dd, day_of_week, HH, MM, SS);
  
  RTC.setTime(buf);
  
}


void split(char *buf, char * delim, char ** output, int* dim) {
  int c = 0;
  
  char* ptr = buf;
  output[c++] = ptr;
  
  while(ptr != NULL)
  {
    ptr = strstr(ptr, delim);
    if (ptr != NULL)
    {
      *ptr = 0;
      output[c++] = ptr + strlen(delim);
      ptr = ptr + strlen(delim);
    }
  }
  
 
  *dim = c;
}



