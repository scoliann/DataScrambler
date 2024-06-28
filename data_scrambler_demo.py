

'''
    ========== Description ==========
    =================================

    Given N data, there are N! different permutations.

    Stirling's approximation gives an estimate for N!
        N! ~= sqrt(2piN) * (N/e)^N

    We can solve for the value of K where N! < 2^K:
        N!       <  2^K
        log2(N!) <  K

        N!       ~= sqrt(2piN) * (N/e)^N
        log2(N!) ~= log2(sqrt(2piN)) + Nlog2(N/e)

        k        <  log2(sqrt(2piN)) + Nlog2(N/e)
        
    Numpy has 2^32 possible random seed values in [0, 2^32).

    Dividing K by 32 will give the number of times we must choose a random seed 
    for the Mersenne Twister and scramble the data, such that brute forcing 
    through the space of random seed permutations is as inefficient as brute 
    forcing all possible permutations of the data itself.

    Alternatively, we can pass through the Mersenne Twister a number of times
    such that brute forcing the process is computationally intractable.  On a 
    modern supercomputer that does 2^60 flops, a 2^K where K = 125 would take 
    roughly 1,000,000 years to brute force.
'''


# Do imports
import cv2
import numpy as np
import hashlib
from tqdm import tqdm


def calculate_k(N):
    return np.log2(np.sqrt(2*np.pi*N)) + (N*np.log2(N/np.e))


def get_hash_int(input_string):
    return int(hashlib.sha256(input_string.encode('utf-8')).hexdigest(), 16)


def scramble(na_data, s_password, b_encrypt, i_k_max=None):

    # Calculate value of k
    f_k = calculate_k(len(na_data))

    # Apply ceiling to k value
    if i_k_max is not None:
        f_k = min(f_k, i_k_max)

    # Calculate Mersenne Twister iterations
    i_mt_iters = int(np.ceil(f_k / 32.0))

    # Apply scramble
    na_scrambled_idxs = np.arange(len(na_data))
    for i in tqdm(range(i_mt_iters)):
    
        # Calculate seed
        i_rng_seed = get_hash_int(f'{s_password}{i}') % (2 ** 32)

        # Set seed
        np.random.seed(i_rng_seed)

        # Get scramble
        np.random.shuffle(na_scrambled_idxs)

    # Apply scramble
    if b_encrypt:
        na_data = na_data[na_scrambled_idxs]
    else:
        na_data = na_data[np.argsort(na_scrambled_idxs)]

    # Return
    return na_data


def main():

    # Define key variables
    s_img_file = 'funky_chicken.png'
    s_password = 'optimal chicken'
    i_k_max = 125

    # Read in image
    na_img = cv2.imread(s_img_file)

    # Flatten image
    na_data = na_img.reshape(-1)

    # Scramble
    na_data_enc = scramble(na_data, s_password, b_encrypt=True, i_k_max=i_k_max)

    # Show and save
    cv2.imshow('Scrambled Image', na_data_enc.reshape(na_img.shape))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('misc/funky_chicken_enc.png', na_data_enc.reshape(na_img.shape))

    # Unscramble
    na_data_dec = scramble(na_data_enc, s_password, b_encrypt=False, i_k_max=i_k_max)

    # Show and save
    cv2.imshow('Unscrambled Image', na_data_dec.reshape(na_img.shape))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('misc/funky_chicken_dec.png', na_data_dec.reshape(na_img.shape))


if __name__ == '__main__':
    main()
