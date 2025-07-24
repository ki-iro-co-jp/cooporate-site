import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/pagination'
import React from 'react';
import { Pagination } from 'swiper/modules'

interface Props {
  imageSrcs: string[];
}

const Slider = ({ imageSrcs }: Props) => {
  return (
    <Swiper
      modules={[Pagination]}
      pagination={{ clickable: true }}
      spaceBetween={10}
      breakpoints={{
        640: {
          slidesPerView: 3,
        },
        768: {
          slidesPerView: 4,
        },
        1024: {
          slidesPerView: 5,
        },
      }}
      slidesPerView={2}
      loop={true}
    >
      {imageSrcs.map((src) => (
        <SwiperSlide
          key={src}
        >
          <div className="slide-container">
            <img src={src} className="slide-image" />
          </div>
        </SwiperSlide>
      ))}
    </Swiper>
  );
};

export default Slider;
