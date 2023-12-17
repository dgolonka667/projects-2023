#include <stdlib.h>
#include <stdio.h>

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

pos make_pos(unsigned int r, unsigned int c) {
    struct pos loc = {r, c};
    return loc;
}


posqueue* posqueue_new() {
    posqueue* queue = (posqueue*)malloc(sizeof(posqueue));
    if (queue != NULL) {
        queue->head = NULL;
        queue->tail = NULL;
        queue->len = 0;
    }
    return queue;
}


void pos_enqueue(posqueue* q, pos p) {
    pq_entry* node = (pq_entry*)malloc(sizeof(pq_entry));
    if (node == NULL) {
        return; 
    }

    node->p = p;
    node->next = NULL;

    if (q->head == NULL) {
        q->head = node;
        q->tail = node;
        q->len = 1;
    } else {
        q->tail->next = node;
        q->tail = node;
        q->len += 1;
    }  
}



pos pos_dequeue(posqueue* q) {
    if (q == NULL || q->head == NULL) {
        printf("Empty queue!\n");
        exit(1);
    }
    pos front = q->head->p;
    pq_entry* temp = q->head;
    q->head = q->head->next;
    q->len -= 1;

    free(temp);
    return front;
}


void posqueue_free(posqueue* q) {
    pq_entry* temp;
    while (q->head) {
        temp = q->head;
        q->head = q->head->next;
        free(temp);
    }
    free(q);
}




