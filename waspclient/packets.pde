/**
 * Status packet : indica al server el estado del waspmote
 *  type = 1
 *  time
 *  xacc
 *  yacc
 *  zacc
 *  batteryLevel
 */
void generate_status_packet(char * msg, unsigned long ep, int x_acc, int y_acc, int z_acc, float batteryLevel, int intCause)
{
  
  char num[20];
  
  sprintf(msg, "1|%ld", ep);
  strncat(msg, "|", 1);

  sprintf(num, "%d", x_acc);
  strncat(msg, num, strlen(num));
  strncat(msg, "|", 1);

  sprintf(num, "%d", y_acc);
  strncat(msg, num, strlen(num));
  strncat(msg, "|", 1);

  sprintf(num, "%d", z_acc);
  strncat(msg, num, strlen(num));
  strncat(msg, "|", 1);

  int entero = (int)(batteryLevel);
  int decimal = (int)((batteryLevel-entero)*100);
  
  sprintf (num, "%d.%d", entero, decimal);
  strncat(msg, num, strlen(num));

  strncat(msg, "|", 1);
  sprintf(num, "%d", intCause);
  strncat(msg, num, strlen(num));
  
  strncat(msg, "\0", strlen("\0"));
}


bool parse_start_packet(char* packet, unsigned long* unixtime, int* deeptime) {
  
  char* parts[10];
  char * delim = "|";
  int dim = 0;
  
  split(packet, delim, parts, &dim);

  if(dim == 3) {

    int type = atoi(parts[0]);
    if(type == 0)
    {
      *unixtime = atol(parts[1]);
      *deeptime = atoi(parts[2]);
      return true;
    }
  }
  return false;
}

