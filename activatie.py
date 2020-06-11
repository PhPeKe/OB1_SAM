# PK TODO
recognized_lexicon_np * lengtes

for word_index in range(fixation - 2, fixation + 3):
    if not recognized_position_flag[word_index]:
        # (-POS-tags)
        desired_length = len(individual_words[word_index])
        # Woorden met juiste lengtes
        # 1. recognized
        # Matrix 1: goede lengte, 0: verkeerde lengte
        # Matrix 2: matrix 1 * recognized, alles wat overblijft is goede lengtem hoogste pakken
        activation_dict = {word: value for word, value in zip(lexicon, lexicon_word_activity_np)}
        activation_sorted = [(word, value) for word, value in sorted(activation_dict.items(),
                                                                     key=lambda item: item[1], reverse=True)
                             if len(word == desired_length)]
        highest = activation_sorted[0]

alldata_recognized_append = all_data[fixation_counter]['recognized words indices'].append
allocated_append = allocated_dict[fixation].append
alldata_truerecognized_append = all_data[fixation_counter]['exact recognized words positions'].append

for word in new_recognized_words:
    my_print('recognized: ',
             amount_of_cycles,
             'cycle,',
             lexicon[word],
             lexicon_word_activity_np[word] / lexicon_thresholds_np[word],
             '(ratio crt. activity to threshold)')
    alldata_recognized_append(word)
    # if yes, words are considered recognized based on similarity of word lengths
    # otherwise, words are considered recognized only if they match exactly
    # TODO think about regressions, should N be excluded from N-1 when regressed?
    # MM: I don't really understand what happens below, but this should be changed anyway
    if pm.similarity_based_recognition:
        # set the recognition flag to any of the words in a similar if they
        # fulfill the word length distance condition
        if is_similar_word_length(individual_words[fixation], lexicon[word]):
            # todo refixations cause problems, because might be that during
            #  refix N+1 is recognized before N
            # maybe just exclude the word during refixation
            # not N-2, N-1,
            if word not in already_allocated and not all_data[fixation_counter]['refixated']:
                if not recognized_position_flag[fixation] or (amount_of_cycles < 1
                                                              and not len(allocated_dict[fixation])):
                    allocated_append(word)
                recognized_position_flag[fixation] = True
                # todo remove last appended before actual saccade, maybe == N+1
                my_print(('+++ 0',
                          lexicon[word],
                          ' recognized instead ',
                          individual_words[fixation]))
        elif shift and fixation + 1 < TOTAL_WORDS and is_similar_word_length(individual_words[fixation + 1],
                                                                             lexicon[word]):
            # not N-2, N-1, N
            if word not in already_allocated:
                recognized_position_flag[fixation + 1] = True
                my_print(('+++ +1',
                          lexicon[word],
                          ' recognized instead ',
                          individual_words[fixation + 1]))
        if fixation - 1 >= 0 and is_similar_word_length(individual_words[fixation - 1], lexicon[word]):
            if word not in allocated_dict[fixation - 2]:
                recognized_position_flag[fixation - 1] = True
                my_print(('+++ -1',
                          lexicon[word],
                          ' recognized instead ',
                          individual_words[fixation - 1]))

        # TODO make vector comparison
        # set the recognition flag for when the exact word is recognized
        # (and store its position in the stimulus) this is also used later
        # to check which words were not recognized
        if individual_to_lexicon_indices[fixation] == word:
            alldata_truerecognized_append(fixation)
            recognized_word_at_position_flag[fixation] = True
            # assert(individual_words[fixation] == lexicon[word])
        elif fixation + 1 < TOTAL_WORDS and individual_to_lexicon_indices[fixation + 1] == word:
            alldata_truerecognized_append(fixation + 1)
            recognized_word_at_position_flag[fixation + 1] = True
            # assert(individual_words[fixation+1] == lexicon[word])
        elif fixation - 1 >= 0 and individual_to_lexicon_indices[fixation - 1] == word:
            alldata_truerecognized_append(fixation - 1)
            recognized_word_at_position_flag[fixation - 1] = True
            # assert(individual_words[fixation-1] == lexicon[word])
        # elif(fixation-2>=0 and individual_to_lexicon_indices[fixation-2]==word):
        #     alldata_truerecognized_append(fixation-2)
        #     recognized_word_at_position_flag[fixation-2] = True
        # elif(fixation+2<TOTAL_WORDS and individual_to_lexicon_indices[fixation+2] == word):
        #     alldata_truerecognized_append(fixation+2)
        #     recognized_word_at_position_flag[fixation] = True
        #     #assert(individual_words[fixation+2] == lexicon[word])
        else:
            # use -1 to represent words that are not in the vicinity
            alldata_truerecognized_append(-1)
    else:
        sys.exit("No dissimilar length recognition")