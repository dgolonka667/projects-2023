#ifndef POS_H
#define POS_H

struct pos {
    unsigned int r, c;
};

typedef struct pos pos;


typedef struct pq_entry pq_entry;

struct pq_entry {
    pos p;
    pq_entry* next;
};


struct posqueue {
    pq_entry *head, *tail;
    unsigned int len;
};

typedef struct posqueue posqueue;

/* Given a row and column number, makes an instance of the pos
struct with r value r and c value c, returns a pos
*/
pos make_pos(unsigned int r, unsigned int c);

/*Creates a new posqueue with an empty head
and tail, returns a pointer to a posqueue*/
posqueue* posqueue_new();

/* Given a pointer to a posqueue, q, and a pos, p,
inserts p into q as a pq_entry at the tail, returns nothing*/
void pos_enqueue(posqueue* q, pos p);

/* Given a pointer to a posqueue, takes out the first
node in the posqueue, returns the pos value, 
and makes the second node in q the head of the queue*/
pos pos_dequeue(posqueue* q);

/* Frees an allocated posqueue and the pq_entries inside, if any*/
void posqueue_free(posqueue* q);

#endif /* POS_H */
